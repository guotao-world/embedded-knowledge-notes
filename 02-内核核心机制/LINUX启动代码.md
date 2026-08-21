# LINUX启动代码

**linux的入口函数是：start_kernel**

**start_kernel主要流程：**

**极早期** lockdep、栈保护、禁用中断

**架构相关** setup_arch：解析硬件信息、建立内存布局

**内存管理** 分阶段完成：zonelists → mm_init → kmem_cache_init_late

**中断与计时** 初始化 IRQ、时钟、定时器，最终开启中断

**调度器** sched_init，preempt_disable

**内核子系统** PID、VFS、cgroup、namespace、proc、security 等

**启动用户态** rest_init() 创建 PID 1 和 PID 2，进入 idle

**PID 0/1/2的作用：**

**注意：**除了 PID 0、1、2 这三个"固定编号"的特殊进程外，**Linux 中并没有其他固定 PID 的特殊进程**。

**PID 0：idle 进程（swapper）**

-   **本质**：一个内核线程，通常称为**idle**或**swapper**。
-   **何时运行**：当 CPU 没有任何其他可运行的进程时，调度器会切换到 idle 进程。它的任务就是执行一条"停机"指令（如hlt），降低 CPU 功耗并等待下一个硬件中断。
-   **启动过程**：在内核初始化时，引导 CPU 从start_kernel→rest_init→cpu_idle()变成 idle 进程。对于多核系统，每个 CPU 都有自己的 idle 线程（但它们不都叫 PID 0，只有引导 CPU 的 idle 进程 PID 为 0）。
-   **其他作用**：在 SMP 系统中，PID 0 也负责在 CPU 热插拔时作为初始线程。

**简单理解**：PID 0 就是**CPU 空闲时运行的"占位"进程**，保证系统在任何时候都有一个进程正在运行（哪怕是"什么也不做"）。

**PID 1：init 进程**

-   **本质**：第一个**用户态**进程，是所有用户进程的祖先。
-   **启动**：由rest_init()通过kernel_thread(kernel_init, ...)创建。它最初是一个内核线程，但很快通过execve加载用户空间的 init 程序（如/sbin/init、/usr/lib/systemd/systemd）。
-   **主要职责**：
-   初始化系统：挂载文件系统、配置网络、启动系统服务（如 cron、sshd、getty 等）。
-   负责系统运行级别的切换（SysV init 风格）。
-   **收养孤儿进程**：任何父进程终止的子进程都会被 PID 1 收养（wait()处理其退出状态，避免僵尸进程）。
-   处理SIGINT、SIGTERM等信号，实现系统重启、关机。

**特点**：如果 PID 1 意外退出（或被 kill），内核会触发 panic，因为失去了用户空间的"根"。

**简单理解**：PID 1 是**系统总管**，负责启动所有其他用户进程，并照顾"无父进程"的孤儿。

**PID 2：kthreadd 内核线程本质**：一个内核线程，专门负责**创建其他内核线程**。**启动**：由rest_init()通过kernel_thread(kthreadd, ...)创建，比 PID 1 稍早。**工作机制**：其他内核模块需要创建内核线程时，不会直接调用do_fork，而是通过kthread_create（或kthread_run）向 kthreadd 发送请求，由 kthreadd 线程统一创建。这样可以集中管理内核线程的创建，避免各种内核路径中的复杂同步问题。**查看方法**：运行ps -ef或pstree可以看到\[kthreadd\]。**简单理解**：PID 2 是**内核线程的"母亲"**，负责生出所有其他内核线程（如ksoftirqd、kworker、kswapd等）。

**三者关系启动顺序**：PID 0（idle）最先存在 →rest_init()创建 PID 2（kthreadd）和 PID 1（init） → PID 2 再创建其他内核线程 → PID 1 启动用户空间。**生命周期**：PID 0 和 PID 2 永远运行（除非系统关机），PID 1 一直运行直到系统关机/重启。**地址空间**：PID 0 和 PID 2 都是内核线程，共享内核地址空间，没有用户空间内存；PID 1 拥有完整的用户态地址空间。

内核中还存在许多**没有固定 PID 编号但非常核心的内核线程**，例如：**ksoftirqd/N**（N 为 CPU 编号）：处理软中断（softirq），如网络数据包处理、高分辨率定时器等。**kworker/N**：执行内核工作队列（workqueue）中的任务，例如设备驱动的延迟处理、电源管理等。**migration/N**：在 SMP 系统中实现 CPU 间任务迁移，支持负载均衡。**rcu_sched / rcu_bh / rcu_preempt**：实现 RCU（Read-Copy-Update）机制的辅助线程。**kswapd**：负责页面回收（swap out），当内存紧张时唤醒。**kdevtmpfs**：管理/dev目录下设备节点的动态创建与删除。**khugepaged**：用于透明大页（THP）的后台整理。**jbd2/sda1-8**：日志文件系统的日志线程（如 ext4）。这些内核线程

**都没有固定的 PID**

，其 PID 是在创建时动态分配的（通常从几十开始递增）。但它们同样至关重要，支撑着内存管理、调度、文件系统等核心功能。