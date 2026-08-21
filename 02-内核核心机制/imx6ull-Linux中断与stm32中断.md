# imx6ull Linux中断与stm32中断

**名称区别：**

**NVIC**

Nested Vectored Interrupt Controller

中文：

嵌套向量中断控制器

**GIC**

Generic Interrupt Controller

中文：

通用中断控制器

**GIC模型：**

硬件中断源（很多个）
↓
中断控制器（GIC）
↓
分两根线给 CPU：
IRQ 线
FIQ 线
↓
CPU 进入：
vector_irq 或 vector_fiq

**Linux驱动里 request_irq() 注册的**

**全部走 vector_irq**

**Linux中断完整路径：**

【汇编层】
vector_irq
↓
__irq_svc
↓
irq_handler
↓
【架构层】
handle_arch_irq
↓
gic_handle_irq
↓
【通用IRQ框架】
generic_handle_irq
↓
__handle_domain_irq
↓
irq_desc↓handle_level_irq / handle_edge_irq↓handle_irq_event ← ★你贴的函数↓【驱动层】action->handler() ← request_irq 注册的函数

**源码对照：stm32:**startup_stm32f429xx.sstm32f4xx_it.c**linux:**arch/arm/kernel/entry-armv.Sdrivers/irqchip/irq-gic.ckernel/irq/handle.c**Linux启动文件：**arch/arm/kernel/head.S 真正的内核启动入口（stext）arch/arm/boot/compressed/head.S 解压 zImage 的部分arch/arm/kernel/entry-armv.S 异常向量表 + 中断/异常入口**Linux ARM（32位）启动流程简要**Bootloader（U-Boot 等）加载 kernel（zImage 或 Image）。跳转到arch/arm/boot/compressed/head.S（如果用了压缩镜像）→ 解压 kernel。跳转到**真正入口**：arch/arm/kernel/head.S的stext。初始化 MMU、页表、CPU、设备树等。最终跳转到start_kernel()（init/main.c）------ 进入通用内核初始化。**entry-armv.S是在第 3 步之后，内核已经启动并设置好向量表时才起作用的。**

```c
int handle_domain_irq(struct irq_domain *domain,                     unsigned int hwirq,                     struct pt_regs *regs){    irq_enter();    irq = irq_find_mapping(domain, hwirq);    generic_handle_irq(irq);    irq_exit();    return 0;}
```

**向量表差异：stm32:**.section .isr_vector,"a",%progbitsg_pfnVectors:    .word _estack                     /* 0x0000 SP初值 */    .word Reset_Handler               /* 0x0004 Reset */    .word NMI_Handler                 /* 0x0008 NMI */    .word HardFault_Handler           /* 0x000C HardFault */    .word MemManage_Handler    .word BusFault_Handler    .word UsageFault_Handler    ...    .word SysTick_Handler
    /* 外部中断 */    .word WWDG_IRQHandler    .word PVD_IRQHandler    .word TAMP_STAMP_IRQHandler    ...    .word TIM2_IRQHandler

**linux:**__vectors_start:    b reset    b undefined    b svc    b prefetch_abort    b data_abort    b reserved    b vector_irq    b vector_fiq**IRQ不区分具体设备！**不管：•UART•GPIO•SPI•I2C全部先进：vector_irq **ARM 的异常向量（从低地址开始）**：Reset（复位）Undefined InstructionPrefetch AbortData AbortAddress ExceptionIRQ（普通中断）**FIQ（快速中断）为什么 FIQ 单独处理？**FIQ 在 ARM 设计上比 IRQ 有更高优先级、更多 banked 寄存器（r8-r12），切换开销更小，适合对实时性要求极高的外设（如某些音频、DMA 等）。

**上下文保存差异：STM32：**Cortex-M硬件自动R0-R3R12LRPCxPSR

**Linux ARM：**entry.S软件保存：R0-R12SPLRPCCPSRBanked regs

**调用链：arch/arm/kernel/entry-armv.S:**W(b) vector_irq**↓**vector_stub irq, IRQ_MODE, 4.long __irq_usr@ 0 (USR_26 / USR_32).long __irq_invalid@ 1 (FIQ_26 / FIQ_32).long __irq_invalid@ 2 (IRQ_26 / IRQ_32).**long __irq_svc**@ 3 (SVC_26 / SVC_32).long __irq_invalid@ 4**↓**__irq_svc:svc_entryirq_handler**↓**.macro irq_handler#ifdef CONFIG_MULTI_IRQ_HANDLERldr r1, =handle_arch_irqmov r0, spadrlr, BSYM(9997f)ldr pc, [r1]#elsearch_irq_handler_default#endif9997:.endm**↓**.macro pabt_helper@ PABORT handler takes pt_regs in r2, fault address in r4 and psr in r5#ifdef MULTI_PABORTldr ip, .LCprocfnsmovlr, pcldr pc, [ip, #PROCESSOR_PABT_FUNC]#elsebl CPU_PABORT_HANDLER#endif.endm**↓**

**drivers/irqchip/irq-gic.c:**void __init gic_init_bases(unsigned int gic_nr, int irq_start, void __iomem *dist_base, void __iomem *cpu_base, u32 percpu_offset, struct device_node *node){.....set_handle_irq(gic_handle_irq);.....}
void __init set_handle_irq(void (*handle_irq)(struct pt_regs *)){if (handle_arch_irq)return;
handle_arch_irq = handle_irq;}**↓drivers\irqchip\irq-gic.c：**static void __exception_irq_entry gic_handle_irq(struct pt_regs *regs){u32 irqstat, irqnr;struct gic_chip_data *gic = &gic_data[0];void __iomem *cpu_base = gic_data_cpu_base(gic);
do {irqstat = readl_relaxed(cpu_base + GIC_CPU_INTACK);irqnr = irqstat & GICC_IAR_INT_ID_MASK;
if (likely(irqnr > 15 && irqnr < 1021)) {handle_domain_irq(gic->domain, irqnr, regs);continue;}if (irqnr < 16) {writel_relaxed(irqstat, cpu_base + GIC_CPU_EOI);#ifdef CONFIG_SMPhandle_IPI(irqnr, regs);#endifcontinue;}break;} while (1);}**↓kernel\irq\irqdesc.c:**int __handle_domain_irq(struct irq_domain *domain, unsigned int hwirq,bool lookup, struct pt_regs *regs){struct pt_regs *old_regs = set_irq_regs(regs);unsigned int irq = hwirq;int ret = 0;
irq_enter();
#ifdef CONFIG_IRQ_DOMAINif (lookup)irq = irq_find_mapping(domain, hwirq);#endif
/* * Some hardware gives randomly wrong interrupts. Rather * than crashing, do something sensible. */if (unlikely(!irq || irq >= nr_irqs)) {ack_bad_irq(irq);ret = -EINVAL;} else {generic_handle_irq(irq);}
irq_exit();set_irq_regs(old_regs);return ret;}#endif
void irq_exit(void){#ifndef __ARCH_IRQ_EXIT_IRQS_DISABLEDlocal_irq_disable();#elseWARN_ON_ONCE(!irqs_disabled());#endif
account_irq_exit_time(current);preempt_count_sub(HARDIRQ_OFFSET);if (!in_interrupt() && local_softirq_pending())**invoke_softirq**();
tick_irq_exit();rcu_irq_exit();trace_hardirq_exit(); /* must be last! */}

**arch/arm/kernel/irq.c：asm_do_IRQ是旧内核使用的：**asmlinkage void __exception_irq_entry asm_do_IRQ(unsigned int irq, struct pt_regs *regs){handle_IRQ(irq, regs);}void handle_IRQ(unsigned int irq, struct pt_regs *regs){__handle_domain_irq(NULL, irq, false, regs);}**↓**int __handle_domain_irq(struct irq_domain *domain, unsigned int hwirq,bool lookup, struct pt_regs *regs){struct pt_regs *old_regs = set_irq_regs(regs);unsigned int irq = hwirq;int ret = 0;
irq_enter();
#ifdef CONFIG_IRQ_DOMAINif (lookup)irq = irq_find_mapping(domain, hwirq);#endif**↓**/* * Some hardware gives randomly wrong interrupts. Rather * than crashing, do something sensible. */if (unlikely(!irq || irq >= nr_irqs)) {ack_bad_irq(irq);ret = -EINVAL;} else {generic_handle_irq(irq);}**↓**irq_exit();set_irq_regs(old_regs);return ret;}#endif

/* * Exit an interrupt context. Process softirqs if needed and possible: */void irq_exit(void){#ifndef __ARCH_IRQ_EXIT_IRQS_DISABLEDlocal_irq_disable();#elseWARN_ON_ONCE(!irqs_disabled());#endif
account_irq_exit_time(current);preempt_count_sub(HARDIRQ_OFFSET);if (!in_interrupt() && local_softirq_pending())invoke_softirq();
tick_irq_exit();rcu_irq_exit();trace_hardirq_exit(); /* must be last! */}