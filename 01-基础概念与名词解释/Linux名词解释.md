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

---

## DWT

**Data Watchpoint and Trace**，数据观察点与跟踪。

ARM Cortex-M 系列处理器中的调试模块，用于设置数据观察点（当访问特定地址时触发调试事件）和程序跟踪。

---

## FAT

**File Allocation Table**，文件分配表。

一种经典的文件系统格式，广泛应用于 U 盘、SD 卡等移动存储设备。优点是兼容性好，几乎所有操作系统都支持；缺点是不支持权限管理、大文件支持有限（FAT32 单文件最大 4GB）。

---

## GPT

**GUID Partition Table**，GUID 分区表。

一种新一代磁盘分区表标准，替代传统的 MBR（Master Boot Record）。支持大于 2TB 的磁盘，最多可创建 128 个分区，分区表有备份，更可靠。通常与 UEFI 配合使用。

---

## MMC

**MultiMedia Card**，多媒体卡控制器。

一种用于管理 MMC/SD/eMMC 等存储设备的控制器接口。MMC 卡是早期的存储卡标准，SD 卡是其演进版本，eMMC 是嵌入式 MMC（将存储芯片和控制器封装在一起）。

---

## MMDC

**Multi Mode DDR Controller**，多模式 DDR 控制器。

NXP i.MX 系列 SoC 中的 DDR 内存控制器，支持 DDR3/DDR3L/LPDDR2 等多种内存类型，负责管理 CPU 与外部 DDR 内存之间的数据传输。

---

## MRC

**Move to Register from Coprocessor**，从协处理器寄存器读取到通用寄存器。

ARM 架构中的汇编指令，用于读取协处理器（如 CP15 系统控制协处理器）的寄存器值到通用寄存器。与 MCR 指令（写协处理器寄存器）配对使用。

```arm
MRC p15, 0, r0, c1, c0, 0   @ 读取 CP15 c1 寄存器到 r0
```

---

## MRS

**Move to Register from Special Register**，从特殊寄存器读取到通用寄存器。

ARM 架构中的汇编指令，用于读取特殊功能寄存器（如 CPSR 当前程序状态寄存器、SPSR 保存的程序状态寄存器）的值到通用寄存器。与 MSR 指令（写特殊寄存器）配对使用。

```arm
MRS r0, CPSR   @ 读取 CPSR 到 r0
```

---

## nmcli

**NetworkManager Command Line Interface**，NetworkManager 命令行接口。

Linux 中 NetworkManager 网络管理服务的命令行工具，用于配置和管理网络连接，包括查看网络状态、配置 IP 地址、连接 WiFi、管理 VPN 等。

```bash
nmcli device status          # 查看网络设备状态
nmcli connection show        # 查看已保存的连接
nmcli radio wifi on          # 开启 WiFi
```

---

## SHA

**Secure Hash Algorithm**，安全哈希算法。

一组密码学哈希函数标准，由美国国家安全局（NSA）设计。常见版本包括 SHA-1（已被破解，不推荐）、SHA-256、SHA-512 等。用于数据完整性校验、数字签名、密码存储等场景。

```bash
sha256sum filename          # 计算文件的 SHA-256 哈希值
```

---

## UEFI

**Unified Extensible Firmware Interface**，统一可扩展固件接口。

一种新一代的固件接口标准，替代传统的 BIOS。提供更强大的启动管理、图形界面、网络启动、安全启动（Secure Boot）等功能。通常使用 GPT 分区表，支持大于 2TB 的磁盘启动。
