# Linux名词解释

#### devm

devm_是 Linux 内核中**设备资源管理 (Device Resource Management)**

#### DAPM

#### Dynamic Audio Power Management (动态音频电源管理)

#### Daemon守护进程

守护进程一定是后台进程，但后台进程不一定是守护进程。**把"守护进程"通俗地理解为"服务"，这是绝对准确且最常用的说法。真正的守护进程（Daemon）一定没有"前台"。**但技术世界里有一个**极其常见且必须知道的特例**，我把它叫做"调试模式"或"临时前台模式"。

#### 严格定义（生产环境）：绝对没有前台

当一个程序被设计成**正式运行的系统服务**时，它必须彻底脱离前台。

-   **没有控制终端**：你在ps -ef里看到它的 TTY 一定是?（问号）。
-   **不占用你的屏幕**：它不会往你的 SSH 终端窗口乱刷数据。
-   **不受 Ctrl+C 影响**：你按 Ctrl+C 发送的是SIGINT（中断信号），这个信号是发给"前台进程组"的。守护进程不在前台，所以**你按 Ctrl+C 根本杀不死它**（得用kill命令）。

**结论**：符合这三点，才叫生产环境下的守护进程。

#### TTY： 是Teletype（电传打字机）

#### FIT：Flattened Image Tree 扁平化镜像树

mkimage -f kernel.its boot.itb

#### ITB：Image Tree Binary FIT 镜像编译后的二进制文件

#### LBA： Logical Block Address 逻辑块地址
