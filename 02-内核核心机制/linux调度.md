# linux 调度

## CFS（Completely Fair Scheduler）

完全公平调度器，Linux 内核默认的进程调度器。

CFS 的核心思想：为每个进程维护一个虚拟运行时间（vruntime），每次调度选择 vruntime 最小的进程运行，从而实现"完全公平"。
