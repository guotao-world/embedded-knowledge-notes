# LINUX 中断

## 一、上半部与下半部

在有些资料中也将上半部和下半部称为**顶半部和底半部**，都是一个意思。

我们在使用 `request_irq` 申请中断的时候注册的中断服务函数属于中断处理的**上半部**，只要中断触发，中断处理函数就会执行。

中断处理函数一定要快点执行完毕，越短越好。但现实中有些中断处理过程比较费时间，必须对其进行拆分，缩小中断处理函数的执行时间。

**举例**：电容触摸屏通过中断通知 SoC 有触摸事件发生，SoC 响应中断，然后通过 I2C 接口读取触摸坐标值并上报给系统。但 I2C 速度最高只有 400 Kbit/s，在中断中通过 I2C 读取数据会浪费时间。可以将 I2C 读取操作暂后执行，中断处理函数仅响应中断、清除中断标志位即可。

此时中断处理过程分为两部分：

- **上半部**：即中断处理函数，处理过程比较快、不会占用很长时间的操作放在上半部完成。
- **下半部**：比较耗时的代码提出来，交给下半部执行，让中断处理函数快进快出。

> Linux 内核将中断分为上半部和下半部的主要目的就是实现中断处理函数的快进快出。对时间敏感、执行速度快的操作放到上半部；剩下的工作放到下半部（比如在上半部将数据拷贝到内存，数据的具体处理放到下半部）。
>
> 至于哪些代码属于上半部、哪些属于下半部，没有明确规定，一切根据实际使用情况判断。

---

## 二、GIC 中断控制器

### Q：GPIO 中断控制器只是起到汇总的作用吗？自身不对 GPIO 中断内容做其他处理？

**A：** 大方向正确，但"只是汇总"不完全准确。更准确地说，GPIO 中断控制器不仅负责汇总多个 GPIO 中断，还负责 GPIO 中断的**检测、配置和管理**；但它不会处理这些中断事件的业务含义。

简单地说，每个外设与 CPU 只通过一两根中断线连接，但每个外设会有一大堆中断。比如 DMA 许多通路都有传输完成中断，这些中断任何一个触发都会统一为 DMA 中断传给 CPU，之后 CPU 对应的外设中断处理函数再去读 DMA 的状态，判断是什么触发了这次中断。

### Q：什么是级联中断控制器（Cascaded Interrupt Controller）？

**A：** 任何能够管理多个中断源，并向上级产生一个中断的硬件模块，都可以被抽象为 `interrupt-controller`。

- GIC / NVIC 是 CPU 级中断控制器
- GPIO / EXTI 这种模块是二级中断控制器

Linux 中的 `interrupt-controller` 不一定代表"最终连接 CPU 的那个控制器"，只要这个硬件模块能够管理一组中断源，就可以被抽象成 `interrupt-controller`。

```
                 CPU
                   |
                 GIC
                   |
          ------------------
          |                |
    GPIO IRQ         PCIe IRQ
          |
     ----------------
     |       |       |
   GPIO0  GPIO1   GPIO2
```

### GIC 概述

GIC 是 ARM 公司给 Cortex-A/R 内核提供的中断控制器，类似 Cortex-M 内核中的 NVIC。

目前 GIC 有 4 个版本：V1~V4。

| 版本 | 适用架构 | 典型内核 |
|------|---------|---------|
| V1 | 最老，已废弃 | — |
| V2 | ARMv7-A（32位） | Cortex-A7、A9、A15 |
| V3/V4 | ARMv8-A/R（64位） | Cortex-A55 等 |

> RK3568 是 Cortex-A55 内核，但本教程主要讲解 GIC V2。GIC V2 最多支持 8 个核。

ARM 会根据 GIC 版本研发不同的 IP 核，半导体厂商直接购买即可。比如 ARM 针对 GIC V2 开发出了 GIC400 这个中断控制器 IP 核。

当 GIC 接收到外部中断信号后报给 ARM 内核，但 ARM 内核只提供了四个信号给 GIC 汇报中断情况：

| 信号 | 含义 |
|------|------|
| VFIQ | 虚拟快速 FIQ |
| VIRQ | 虚拟快速 IRQ |
| FIQ | 快速中断 |
| IRQ | 外部中断 |

VFIQ 和 VIRQ 针对虚拟化，不讨论虚拟化的话剩下 FIQ 和 IRQ，本教程只使用 IRQ。相当于 GIC 最终向 ARM 内核上报一个 IRQ 信号。

---

## 三、常见问题

### Q：`disable_irq_nosync` 和 `disable_irq` 区别？

**A：**

- `disable_irq()` 会等待正在执行的中断处理函数结束
- `disable_irq_nosync()` 是关闭后立即返回

如果在中断处理函数中调用 `disable_irq()`，可能出现死等：当前 IRQ 正在执行，`disable_irq()` 等待当前 IRQ 结束，但当前函数还没返回。此时必须使用 `disable_irq_nosync()`。

> `disable_irq_nosync()` 只是"暂时关掉中断开关"，不会释放资源；资源一直保持到 `free_irq()` 被调用，用于很多需要反复开启中断的场景。

### Q：`disable_irq()` 有什么意义？

**A：** 目的是等中断执行完后再释放资源。

- **场景一（多核系统）**：假设 CPU0 正在操作网卡资源，CPU1 认为 IRQ 已经关闭，对资源进行释放，可能导致 CPU0 继续访问已释放的内存，从而系统崩溃。
- **场景二（卸载驱动）**：避免中断访问卸载后的资源。

### Q：驱动上报事件后，用户层 read 的数据就自动变成了事件对吗？

**A：** 驱动调用 `input_report_key()` 上报事件后，事件会进入 Linux input 子系统的事件队列，用户层 `read()` 读取的就是这个队列里的 `struct input_event` 数据。

不是说用户层的 `read()` 数据"自动变成"事件，而是 input 框架帮你完成了从内核事件到字符设备数据流的转换。

### Q：input 子系统并没有简化按键检测的流程，只是把各个输入流程规范化了，对吗？

**A：** 理解基本正确，而且抓住了 input 子系统设计的核心。

更准确地说，input 子系统不是为了简化"硬件输入检测过程"，而是为了简化"输入设备驱动和应用之间的交互"，同时把各种输入设备的事件模型统一。它主要解决的是软件架构问题，不是减少 GPIO 检测、消抖、中断这些硬件处理工作。

---

## 四、i.MX6ULL Linux 中断与 STM32 中断对比

### 名称区别

| 平台 | 缩写 | 全称 | 中文 |
|------|------|------|------|
| STM32 (Cortex-M) | NVIC | Nested Vectored Interrupt Controller | 嵌套向量中断控制器 |
| Linux (Cortex-A) | GIC | Generic Interrupt Controller | 通用中断控制器 |

### GIC 模型

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

## 五、Linux 中断完整路径

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
handle_irq_event      ← ★ 核心函数
    ↓
【驱动层】
action->handler()     ← request_irq 注册的函数
```

---

## 六、源码对照

| 层级 | STM32 | Linux |
|------|-------|-------|
| 启动/向量表 | `startup_stm32f429xx.s` | `arch/arm/kernel/entry-armv.S` |
| 中断处理 | `stm32f4xx_it.c` | `drivers/irqchip/irq-gic.c` |
| 通用框架 | — | `kernel/irq/handle.c` |

### Linux 启动文件

| 文件 | 作用 |
|------|------|
| `arch/arm/kernel/head.S` | 真正的内核启动入口（`stext`） |
| `arch/arm/boot/compressed/head.S` | 解压 zImage 的部分 |
| `arch/arm/kernel/entry-armv.S` | 异常向量表 + 中断/异常入口 |

### Linux ARM（32位）启动流程

1. Bootloader（U-Boot 等）加载 kernel（zImage 或 Image）
2. 跳转到 `arch/arm/boot/compressed/head.S`（如果用了压缩镜像）→ 解压 kernel
3. 跳转到真正入口：`arch/arm/kernel/head.S` 的 `stext`
4. 初始化 MMU、页表、CPU、设备树等
5. 最终跳转到 `start_kernel()`（`init/main.c`）—— 进入通用内核初始化

> `entry-armv.S` 是在第 3 步之后，内核已经启动并设置好向量表时才起作用的。

### `handle_domain_irq` 源码

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

## 七、向量表差异

### STM32

```asm
.section .isr_vector,"a",%progbits
g_pfnVectors:
    .word _estack                  /* 0x0000 SP初值 */
    .word Reset_Handler            /* 0x0004 Reset */
    .word NMI_Handler              /* 0x0008 NMI */
    .word HardFault_Handler        /* 0x000C HardFault */
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

### Linux ARM

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

> **IRQ 不区分具体设备！** 不管是 UART、GPIO、SPI 还是 I2C，全部先进 `vector_irq`。

ARM 的异常向量（从低地址开始）：

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

## 八、上下文保存差异

| 平台 | 保存方式 | 保存内容 |
|------|---------|---------|
| STM32 (Cortex-M) | 硬件自动 | R0-R3、R12、LR、PC、xPSR |
| Linux ARM | 软件保存（entry.S） | R0-R12、SP、LR、PC、CPSR、Banked regs |

---

## 九、调用链源码

### 汇编层：`arch/arm/kernel/entry-armv.S`

```asm
W(b) vector_irq
    ↓
vector_stub irq, IRQ_MODE, 4
    .long __irq_usr       @ 0  (USR_26 / USR_32)
    .long __irq_invalid   @ 1  (FIQ_26 / FIQ_32)
    .long __irq_invalid   @ 2  (IRQ_26 / IRQ_32)
    .long __irq_svc       @ 3  (SVC_26 / SVC_32)
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

### 架构层：`drivers/irqchip/irq-gic.c`

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

### 通用框架：`kernel/irq/irqdesc.c`

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

    /*
     * Some hardware gives randomly wrong interrupts.  Rather
     * than crashing, do something sensible.
     */
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

### 旧内核接口：`arch/arm/kernel/irq.c`

`asm_do_IRQ` 是旧内核使用的：

```c
asmlinkage void __exception_irq_entry
asm_do_IRQ(unsigned int irq, struct pt_regs *regs)
{
    handle_IRQ(irq, regs);
}

void handle_IRQ(unsigned int irq, struct pt_regs *regs)
{
    __handle_domain_irq(NULL, irq, false, regs);
}
```

调用路径：

```
asm_do_IRQ()
    ↓
handle_IRQ()
    ↓
__handle_domain_irq(NULL, irq, false, regs)
    ↓
irq_enter()
    ↓
irq_find_mapping()  (if lookup)
    ↓
generic_handle_irq(irq)
    ↓
irq_exit()
```

`irq_exit()` 中会检查是否有软中断待处理，如果有则调用 `invoke_softirq()` 执行下半部。
