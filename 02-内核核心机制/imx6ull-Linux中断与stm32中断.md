# imx6ull Linux 中断与 stm32 中断

## 一、名称区别

| 名称 | 全称 | 中文 |
|------|------|------|
| NVIC | Nested Vectored Interrupt Controller | 嵌套向量中断控制器 |
| GIC | Generic Interrupt Controller | 通用中断控制器 |

---

## 二、GIC 模型

```
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
```

> Linux 驱动里 `request_irq()` 注册的全部走 `vector_irq`。

---

## 三、Linux 中断完整路径

```
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
【通用 IRQ 框架】
generic_handle_irq
    ↓
__handle_domain_irq
    ↓
irq_desc
    ↓
handle_level_irq / handle_edge_irq
    ↓
handle_irq_event   ← 核心函数
    ↓
【驱动层】
action->handler()   ← request_irq 注册的函数
```

---

## 四、源码对照

| 平台 | 启动/中断文件 |
|------|-------------|
| STM32 | `startup_stm32f429xx.s`、`stm32f4xx_it.c` |
| Linux | `arch/arm/kernel/entry-armv.S`、`drivers/irqchip/irq-gic.c`、`kernel/irq/handle.c` |

### Linux 启动文件

| 文件 | 作用 |
|------|------|
| `arch/arm/kernel/head.S` | 真正的内核启动入口（stext） |
| `arch/arm/boot/compressed/head.S` | 解压 zImage 的部分 |
| `arch/arm/kernel/entry-armv.S` | 异常向量表 + 中断/异常入口 |

### Linux ARM（32 位）启动流程

1. Bootloader（U-Boot 等）加载 kernel（zImage 或 Image）
2. 跳转到 `arch/arm/boot/compressed/head.S`（如果用了压缩镜像）→ 解压 kernel
3. 跳转到真正入口：`arch/arm/kernel/head.S` 的 `stext`
4. 初始化 MMU、页表、CPU、设备树等
5. 最终跳转到 `start_kernel()`（`init/main.c`）—— 进入通用内核初始化

> `entry-armv.S` 是在第 3 步之后，内核已经启动并设置好向量表时才起作用的。

---

## 五、核心函数

```c
int handle_domain_irq(struct irq_domain *domain,
                      unsigned int hwirq,
                      struct pt_regs *regs)
{
    irq_enter();
    irq = irq_find_mapping(domain, hwirq);
    generic_handle_irq(irq);
    irq_exit();
    return 0;
}
```

---

## 六、向量表差异

### STM32

```asm
.section .isr_vector,"a",%progbits
g_pfnVectors:
    .word _estack              /* 0x0000 SP 初值 */
    .word Reset_Handler        /* 0x0004 Reset */
    .word NMI_Handler          /* 0x0008 NMI */
    .word HardFault_Handler    /* 0x000C HardFault */
    .word MemManage_Handler
    .word BusFault_Handler
    .word UsageFault_Handler
    ...
    .word SysTick_Handler

    /* 外部中断 */
    .word WWDG_IRQHandler
    .word PVD_IRQHandler
    .word TAMP_STAMP_IRQHandler
    ...
    .word TIM2_IRQHandler
```

### Linux

```asm
__vectors_start:
    b reset
    b undefined
    b svc
    b prefetch_abort
    b data_abort
    b reserved
    b vector_irq
    b vector_fiq
```

> IRQ 不区分具体设备！不管 UART、GPIO、SPI、I2C，全部先进 `vector_irq`。

### ARM 异常向量（从低地址开始）

1. Reset（复位）
2. Undefined Instruction
3. Prefetch Abort
4. Data Abort
5. Address Exception
6. IRQ（普通中断）
7. FIQ（快速中断）

### 为什么 FIQ 单独处理？

FIQ 在 ARM 设计上比 IRQ 有更高优先级、更多 banked 寄存器（r8-r12），切换开销更小，适合对实时性要求极高的外设（如某些音频、DMA 等）。

---

## 七、上下文保存差异

| 平台 | 保存方式 | 保存内容 |
|------|---------|---------|
| STM32 | Cortex-M 硬件自动 | R0-R3、R12、LR、PC、xPSR |
| Linux ARM | entry.S 软件保存 | R0-R12、SP、LR、PC、CPSR、Banked regs |

---

## 八、调用链详解

### 汇编层（entry-armv.S）

```
W(b) vector_irq
    ↓
vector_stub irq, IRQ_MODE, 4
    .long __irq_usr       @ 0 (USR_26 / USR_32)
    .long __irq_invalid   @ 1 (FIQ_26 / FIQ_32)
    .long __irq_invalid   @ 2 (IRQ_26 / IRQ_32)
    .long __irq_svc       @ 3 (SVC_26 / SVC_32)
    .long __irq_invalid   @ 4
    ↓
__irq_svc:
    svc_entry
    irq_handler
    ↓
.macro irq_handler
#ifdef CONFIG_MULTI_IRQ_HANDLER
    ldr r1, =handle_arch_irq
    mov r0, sp
    adr lr, BSYM(9997f)
    ldr pc, [r1]
#else
    arch_irq_handler_default
#endif
9997:
.endm
```

### 架构层（irq-gic.c）

```c
void __init gic_init_bases(unsigned int gic_nr, int irq_start,
    void __iomem *dist_base, void __iomem *cpu_base,
    u32 percpu_offset, struct device_node *node)
{
    .....
    set_handle_irq(gic_handle_irq);
    .....
}

void __init set_handle_irq(void (*handle_irq)(struct pt_regs *))
{
    if (handle_arch_irq)
        return;
    handle_arch_irq = handle_irq;
}
```

```c
static void __exception_irq_entry gic_handle_irq(struct pt_regs *regs)
{
    u32 irqstat, irqnr;
    struct gic_chip_data *gic = &gic_data[0];
    void __iomem *cpu_base = gic_data_cpu_base(gic);

    do {
        irqstat = readl_relaxed(cpu_base + GIC_CPU_INTACK);
        irqnr = irqstat & GICC_IAR_INT_ID_MASK;

        if (likely(irqnr > 15 && irqnr < 1021)) {
            handle_domain_irq(gic->domain, irqnr, regs);
            continue;
        }
        if (irqnr < 16) {
            writel_relaxed(irqstat, cpu_base + GIC_CPU_EOI);
#ifdef CONFIG_SMP
            handle_IPI(irqnr, regs);
#endif
            continue;
        }
        break;
    } while (1);
}
```

### 通用 IRQ 框架（irqdesc.c）

```c
int __handle_domain_irq(struct irq_domain *domain, unsigned int hwirq,
                        bool lookup, struct pt_regs *regs)
{
    struct pt_regs *old_regs = set_irq_regs(regs);
    unsigned int irq = hwirq;
    int ret = 0;

    irq_enter();

#ifdef CONFIG_IRQ_DOMAIN
    if (lookup)
        irq = irq_find_mapping(domain, hwirq);
#endif

    if (unlikely(!irq || irq >= nr_irqs)) {
        ack_bad_irq(irq);
        ret = -EINVAL;
    } else {
        generic_handle_irq(irq);
    }

    irq_exit();
    set_irq_regs(old_regs);
    return ret;
}
```

```c
void irq_exit(void)
{
#ifndef __ARCH_IRQ_EXIT_IRQS_DISABLED
    local_irq_disable();
#else
    WARN_ON_ONCE(!irqs_disabled());
#endif

    account_irq_exit_time(current);
    preempt_count_sub(HARDIRQ_OFFSET);
    if (!in_interrupt() && local_softirq_pending())
        invoke_softirq();

    tick_irq_exit();
    rcu_irq_exit();
    trace_hardirq_exit(); /* must be last! */
}
```

> `irq_exit()` 中会检查是否有软中断待处理，如果有则调用 `invoke_softirq()` 处理软中断（下半部）。
