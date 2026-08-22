# STM32 与 LINUX 的任务调度方式

## 一、本质对比

![STM32 与 Linux 调度对比](../images/image26.png)

---

## 二、STM32 RTOS（FreeRTOS）详细流程

### 最常见情况

1. **SysTick 中断**（Tick ISR）触发：增加 tick 计数
2. 检查是否有任务超时、更高优先级任务就绪
3. 如果需要切换 → **置位 PendSV pending bit**（不立即切换）
4. **SysTick ISR 正常退出**（此时还运行在原来的任务上下文）
5. **PendSV 中断**（优先级最低）立即触发：
   - 保存当前任务的寄存器（R4~R11 等）到其栈中
   - 保存栈指针到 TCB（任务控制块）
   - 调用调度器选择下一个要运行的任务
   - 加载新任务的栈指针
   - 恢复新任务的寄存器
   - **从 PendSV 中断返回**（硬件自动恢复 R0~R3、PC、PSR 等）

> 上下文切换完全在 PendSV Handler 中完成，切换完毕后直接退出中断，CPU 开始执行新任务。

### 为什么用 PendSV？

因为它优先级最低，可以保证在所有其他中断处理完之后再进行切换，避免在高优先级中断中切换上下文导致问题。

---

## 三、Linux 内核调度流程

1. **Timer 中断**触发：更新 jiffies，调用 `scheduler_tick()`
2. 如果需要抢占 → 设置当前进程的 `TIF_NEED_RESCHED` 标志
3. **Timer 中断即将退出**时（或系统调用返回、异常返回时）：
   - 检查 `need_resched` 标志
   - 如果置位 → 调用 `__schedule()`
4. 在 `__schedule()` 中执行 `context_switch()`（切换 mm_struct、寄存器、栈等）
5. **切换完成后**，从中断/异常返回到新进程的用户态或内核态

> Linux 不会在 timer 中断里面直接完整执行上下文切换，而是"懒切换"（lazy），在安全时机（返回用户空间路径）才真正切换。

---

## 四、Linux 内核调度详细执行流程（以 Timer 中断为例）

### 1. 硬件产生 Timer 中断

CPU 自动保存部分寄存器，跳转到内核的中断入口（entry code），进入**中断上下文**。

### 2. 执行中断处理函数（ISR）

- 更新 jiffies
- 调用 `scheduler_tick()`
- 如果发现需要抢占，给当前进程设置标志：`TIF_NEED_RESCHED`
- 注意：这里不会直接调用 `schedule()` 做上下文切换，只是打个标记

### 3. 中断处理函数执行完毕

开始进入**中断返回路径**（ret_from_intr 或现代内核的 exit_to_user_mode 等）。

### 4. 在返回路径的最后阶段检查标志

内核检查 `current->thread_info->flags` 中是否有 `TIF_NEED_RESCHED`：

- 如果有，并且即将返回用户态（最常见情况），则调用 `__schedule()`
- 在 `__schedule()` 中完成真正的 `context_switch`（切换页表、切换寄存器、切换栈等）

### 5. 切换完成后

执行 `iret`（或 `sysret`/`iretq`）指令，真正退出中断，CPU 开始执行新进程的用户态代码。

> 调度是在"出口统一处理"：任何中断返回时都可能触发调度，不仅仅是定时器。IO 中断、网络中断、系统调用返回、异常返回都可能触发 `schedule()`。

---

## 五、中断返回路径

```
1. 中断发生（硬件）
   → CPU 进入内核模式，保存现场（寄存器、返回地址等）
        ↓
2. 中断入口代码（assembly）
   → 保存更多上下文，准备调用 C 函数
        ↓
3. 执行 ISR（Interrupt Service Routine）
   ← 这就是我们常说的"中断处理函数"
        ↓
4. ISR 执行完毕
        ↓
5. 【返回路径】（Return Path）
   ← 检查 need_resched，可能触发调度
        ↓
6. 真正退出中断（执行 iret / eret 等指令）
   → 返回到被打断的地方（用户态或内核态）
```

---

## 六、对比总结

| 特性 | STM32 (FreeRTOS) | Linux |
|------|------------------|-------|
| 切换时机 | SysTick 中置位 PendSV，在 PendSV 中切换 | Timer 中断中置位标志，在中断返回路径中切换 |
| 切换位置 | PendSV Handler | `__schedule()` → `context_switch()` |
| 切换策略 | 优先级抢占 | CFS 完全公平调度 |
| 中断中切换 | PendSV 优先级最低，等其他中断完 | 不在中断中直接切换，懒切换到返回路径 |
