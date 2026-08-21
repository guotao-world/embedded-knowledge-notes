# STM32与LINUX的任务调度方式

**0、本质对比：**

![](../images/image26.png)

**一、STM32 RTOS（FreeRTOS）详细流程（最常见情况）**

-   **SysTick 中断**（Tick ISR）触发：增加 tick 计数
-   检查是否有任务超时、更高优先级任务就绪
-   如果需要切换 →**置位 PendSV pending bit**（不立即切换）

**SysTick ISR 正常退出**（此时还运行在原来的任务上下文）

-   **PendSV 中断**（优先级最低）立即触发：保存当前任务的寄存器（R4~R11 等）到其栈中
-   保存栈指针到 TCB（任务控制块）
-   调用调度器选择下一个要运行的任务
-   加载新任务的栈指针
-   恢复新任务的寄存器
-   **从 PendSV 中断返回**（硬件自动恢复 R0~R3、PC、PSR 等）

→**上下文切换完全在 PendSV Handler 中完成**，切换完毕后直接退出中断，CPU 开始执行**新任务**。

**为什么用 PendSV？**因为它优先级最低，可以保证在所有其他中断处理完之后再进行切换，避免在高优先级中断中切换上下文导致问题。

**二、Linux 内核调度流程Timer 中断**触发：更新 jiffies调用scheduler_tick()如果需要抢占 → 设置当前进程的TIF_NEED_RESCHED标志**Timer 中断即将退出**时（或系统调用返回、异常返回时）：检查need_resched标志如果置位 → 调用__schedule()在__schedule()中执行context_switch()（切换 mm_struct、寄存器、栈等）**切换完成后**，从中断/异常返回到**新进程**的用户态或内核态。Linux**不会在 timer 中断里面直接完整执行上下文切换**，而是"懒切换"（lazy），在安全时机（返回用户空间路径）才真正切换。

**三、Linux 内核调度详细执行流程（以 Timer 中断为例）硬件产生 Timer 中断**CPU 自动保存部分寄存器，跳转到内核的中断入口（entry code），进入**中断上下文**。**执行中断处理函数（ISR）**更新jiffies调用scheduler_tick()如果发现需要抢占，就给**当前进程**设置一个标志：TIF_NEED_RESCHED（需要重新调度）→**注意**：这里**不会**直接调用schedule()做上下文切换，只是**打个标记**。**中断处理函数执行完毕**现在开始进入**中断返回路径**（ret_from_intr或现代内核的exit_to_user_mode/prepare_exit_to_usermode等）。**在返回路径的最后阶段检查标志**（这就是"Timer 中断即将退出时"）：内核检查current->thread_info->flags中是否有TIF_NEED_RESCHED如果有，并且即将返回**用户态**（最常见情况），则调用__schedule()在__schedule()中完成真正的**context_switch**（切换页表、切换寄存器、切换栈等）**切换完成后**，执行iret（或sysret/iretq）指令，**真正退出中断**，CPU 开始执行**新进程**的用户态代码。**注意：调度是在"出口统一处理"**任何中断返回时，都可能触发调度（任何中断退出 → 都会进入 return path检查是否需要调度）不仅仅是定时器：IO 中断网络中断系统调用返回异常返回都可能触发：schedule()

**四、中断返回路径1. 中断发生（硬件）** → CPU 进入内核模式，保存现场（寄存器、返回地址等） ↓**2. 中断入口代码（assembly）** → 保存更多上下文，准备调用 C 函数 ↓**3. 执行 ISR（Interrupt Service Routine）** ← 这就是我们常说的"中断处理函数" ↓**4. ISR 执行完毕 ↓5. 【返回路径】（Return Path）** ← 这里就是你不理解的部分 ↓**6. 真正退出中断（执行 iret / eret 等指令）**，返回到被打断的地方（用户态或内核态）