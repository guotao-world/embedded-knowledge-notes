# 嵌入式 Linux 学习笔记

> 本仓库记录了嵌入式 Linux 开发学习过程中的知识点、代码示例和调试经验，涵盖驱动开发、内核机制、ALSA 音频、设备树、编译构建等多个主题。

## 📑 目录

### 基础概念与名词解释

- [Linux名词解释](./01-基础概念与名词解释/Linux名词解释.md)
- [嵌入式linux命令](./01-基础概念与名词解释/嵌入式linux命令.md)

### 内核核心机制

- [LINUX并发与竞争](./02-内核核心机制/LINUX并发与竞争.md)
- [LINUX等待队列](./02-内核核心机制/LINUX等待队列.md)
- [linux定时器](./02-内核核心机制/linux定时器.md)
- [LINUX启动代码](./02-内核核心机制/LINUX启动代码.md)
- [LINUX初始化的宏](./02-内核核心机制/LINUX初始化的宏.md)
- [imx6ull Linux中断与stm32中断](./02-内核核心机制/imx6ull-Linux中断与stm32中断.md)
- [STM32与LINUX的任务调度方式](./02-内核核心机制/STM32与LINUX的任务调度方式.md)
- [页表](./02-内核核心机制/页表.md)
- [LINUX中断](./02-内核核心机制/LINUX中断.md)
- [linux调度](./02-内核核心机制/linux调度.md)
- [linux用户态内核态](./02-内核核心机制/linux用户态内核态.md)
- [linux启动流程](./02-内核核心机制/linux启动流程.md)

### 驱动开发基础

- [linux ioctl操作](./03-驱动开发基础/linux-ioctl操作.md)
- [安装内核模块命令](./03-驱动开发基础/安装内核模块命令.md)
- [GPIO子系统描述](./03-驱动开发基础/GPIO子系统描述.md)
- [linux驱动设备号](./03-驱动开发基础/linux驱动设备号.md)
- [static关键字与const关键字](./03-驱动开发基础/static关键字与const关键字.md)
- [设备树的概念](./03-驱动开发基础/设备树的概念.md)
- [Linux驱动核心骨架](./03-驱动开发基础/Linux驱动核心骨架.md)
- [linux串口驱动](./03-驱动开发基础/linux串口驱动.md)
- [pinptr子系统与GPIO子系统](./03-驱动开发基础/pinptr子系统与GPIO子系统.md)
- [LINUX总线注册时间](./03-驱动开发基础/LINUX总线注册时间.md)
- [linux总线驱动模型设备创建顺序](./03-驱动开发基础/linux总线驱动模型设备创建顺序.md)
- [设备树解析流程](./03-驱动开发基础/设备树解析流程.md)
- [regmap示例](./03-驱动开发基础/regmap示例.md)
- [注册设备与创建设备的区别](./03-驱动开发基础/注册设备与创建设备的区别.md)
- [linux i2c读写数据的示例](./03-驱动开发基础/linux-i2c读写数据的示例.md)
- [linux时钟](./03-驱动开发基础/linux时钟.md)
- [regmap寄存器访问抽象框架](./03-驱动开发基础/regmap寄存器访问抽象框架.md)
- [linux总线驱动模型核心例程](./03-驱动开发基础/linux总线驱动模型核心例程.md)
- [paltform总线](./03-驱动开发基础/paltform总线.md)
- [lLinux设备树的节点device_node](./03-驱动开发基础/lLinux设备树的节点device_node.md)
- [input子系统](./03-驱动开发基础/input子系统.md)
- [Platform总线与其他总线的区别](./03-驱动开发基础/Platform总线与其他总线的区别.md)

### ALSA音频驱动

- [linux音频驱动编译调试流程](./04-ALSA音频驱动/linux音频驱动编译调试流程.md)
- [ALSA的设备树示例](./04-ALSA音频驱动/ALSA的设备树示例.md)
- [ALSA学习路线](./04-ALSA音频驱动/ALSA学习路线.md)
- [音频数据结构层次](./04-ALSA音频驱动/音频数据结构层次.md)
- [Machine驱动](./04-ALSA音频驱动/Machine驱动.md)
- [linux音频栈](./04-ALSA音频驱动/linux音频栈.md)
- [LINUX开发板录放指令](./04-ALSA音频驱动/LINUX开发板录放指令.md)
- [linux声卡 ALSA](./04-ALSA音频驱动/linux声卡-ALSA.md)

### 编译与构建系统

- [编译设备树](./05-编译与构建系统/编译设备树.md)
- [编译内核](./05-编译与构建系统/编译内核.md)
- [编译imx6ull linux应用app](./05-编译与构建系统/编译imx6ull-linux应用app.md)
- [Kconfig讲解](./05-编译与构建系统/Kconfig讲解.md)
- [linux源码顶层结构](./05-编译与构建系统/linux源码顶层结构.md)
- [Source Insight使用方法](./05-编译与构建系统/Source-Insight使用方法.md)
- [linux驱动编译流程](./05-编译与构建系统/linux驱动编译流程.md)
- [imx6ull linux驱动makefile模板](./05-编译与构建系统/imx6ull-linux驱动makefile模板.md)
- [嵌入式Linux编译工具链的不同](./05-编译与构建系统/嵌入式Linux编译工具链的不同.md)

### U-Boot与启动

- [uboot启动linux内核指令](./06-U-Boot与启动/uboot启动linux内核指令.md)
- [Secure Boot 的核心思想](./06-U-Boot与启动/Secure-Boot-的核心思想.md)

### 开发板操作与环境

- [linux备份emmc镜像](./07-开发板操作与环境/linux备份emmc镜像.md)
- [linux对内存卡做镜像](./07-开发板操作与环境/linux对内存卡做镜像.md)
- [LINUX开发板中F4或其他按键失效](./07-开发板操作与环境/LINUX开发板中F4或其他按键失效.md)
- [linux文件目录](./07-开发板操作与环境/linux文件目录.md)
- [挂载U盘](./07-开发板操作与环境/挂载U盘.md)
- [RK3568源码结构](./07-开发板操作与环境/RK3568源码结构.md)
- [rk3568_linux_sdk](./07-开发板操作与环境/rk3568_linux_sdk.md)
- [硬盘分区规范](./07-开发板操作与环境/硬盘分区规范.md)
- [linux nfs服务器](./07-开发板操作与环境/linux-nfs服务器.md)
- [IP配置](./07-开发板操作与环境/IP配置.md)
- [ssh](./07-开发板操作与环境/ssh.md)
- [chmod指令](./07-开发板操作与环境/chmod指令.md)

### C语言与软件设计

- [C语言常见问题](./08-C语言与软件设计/C语言常见问题.md)
- [低性能MCU软件设计分层](./08-C语言与软件设计/低性能MCU软件设计分层.md)

### 图形系统

- [图形界面QT等](./09-图形系统/图形界面QT等.md)
- [LINUX图形系统本质](./09-图形系统/LINUX图形系统本质.md)

### 其他

- [智能体运行方式](./10-其他/智能体运行方式.md)
- [yml文件讲解](./10-其他/yml文件讲解.md)

---

## 📝 说明

- 本笔记基于学习过程整理，内容可能存在不准确之处，欢迎指正
- 代码示例主要基于 Linux Kernel 4.19，适用于 ARM 架构嵌入式平台
- 图片资源存放在 `images/` 目录下
