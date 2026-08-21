# Linux 名词解释

## devm

`devm_` 是 Linux 内核中**设备资源管理（Device Resource Management）**的前缀。

使用 `devm_` 系列函数分配的资源（如内存、GPIO、中断等）会在设备移除时自动释放，无需手动在 `remove` 函数中清理。

---

## DAPM

**Dynamic Audio Power Management**，动态音频电源管理。

ALSA SoC 框架中的子系统，用于根据音频路径的使用情况动态开关 codec 内部的模块电源，降低功耗。

---

## Daemon 守护进程

守护进程一定是后台进程，但后台进程不一定是守护进程。

> 把"守护进程"通俗地理解为"服务"，这是绝对准确且最常用的说法。真正的守护进程（Daemon）一定没有"前台"。

但技术世界里有一个极其常见且必须知道的特例——"调试模式"或"临时前台模式"。

### 严格定义（生产环境）：绝对没有前台

当一个程序被设计成正式运行的系统服务时，它必须彻底脱离前台：

- **没有控制终端**：在 `ps -ef` 里看到它的 TTY 一定是 `?`（问号）
- **不占用你的屏幕**：它不会往你的 SSH 终端窗口乱刷数据
- **不受 Ctrl+C 影响**：Ctrl+C 发送的是 `SIGINT`（中断信号），这个信号是发给"前台进程组"的。守护进程不在前台，所以按 Ctrl+C 根本杀不死它（得用 `kill` 命令）

**结论**：符合这三点，才叫生产环境下的守护进程。

---

## TTY

**Teletype**，电传打字机。

在 Linux 中泛指终端设备，包括物理串口、虚拟终端、伪终端（PTY）等。`ps -ef` 输出中的 TTY 列即表示进程关联的终端设备。

---

## FIT

**Flattened Image Tree**，扁平化镜像树。

一种可将内核、设备树、ramdisk 等多个镜像打包成一个文件的格式，通过 `.its` 配置文件描述，使用 `mkimage` 工具生成。

```bash
mkimage -f kernel.its boot.itb
```

---

## ITB

**Image Tree Binary**，FIT 镜像编译后的二进制文件。

即 `.its` 配置文件经过 `mkimage` 编译后生成的 `.itb` 文件，可被 U-Boot 直接引导。

---

## LBA

**Logical Block Address**，逻辑块地址。

存储设备（硬盘、eMMC、SD 卡等）对上层提供的统一寻址方式，以扇区（通常 512 字节）为单位。`dd` 命令中的 `seek`、`skip` 参数即使用 LBA 寻址。
