# 嵌入式 Linux 学习笔记

> 作为小菜鸡，本仓库记录了本人嵌入式 Linux 开发学习过程中的知识点、代码示例和调试经验，欢迎指正。

## 📑 目录

<!-- TOC START -->
### 01-基础概念与名词解释

- [Linux 名词解释](./01-基础概念与名词解释/Linux名词解释.md)
- [嵌入式 Linux 常用命令](./01-基础概念与名词解释/嵌入式linux命令.md)

### 02-内核核心机制

- [LINUX 中断](./02-内核核心机制/LINUX中断.md)
- [LINUX 初始化的宏](./02-内核核心机制/LINUX初始化的宏.md)
- [LINUX 启动代码](./02-内核核心机制/LINUX启动代码.md)
- [LINUX 并发与竞争](./02-内核核心机制/LINUX并发与竞争.md)
- [LINUX 等待队列](./02-内核核心机制/LINUX等待队列.md)
- [STM32 与 LINUX 的任务调度方式](./02-内核核心机制/STM32与LINUX的任务调度方式.md)
- [imx6ull Linux 中断与 stm32 中断](./02-内核核心机制/imx6ull-Linux中断与stm32中断.md)
- [linux 启动流程](./02-内核核心机制/linux启动流程.md)
- [linux 定时器](./02-内核核心机制/linux定时器.md)
- [linux 用户态内核态](./02-内核核心机制/linux用户态内核态.md)
- [linux 调度](./02-内核核心机制/linux调度.md)
- [页表](./02-内核核心机制/页表.md)

### 03-驱动开发基础

- [GPIO 子系统描述](./03-驱动开发基础/GPIO子系统描述.md)
- [LINUX 总线注册时间](./03-驱动开发基础/LINUX总线注册时间.md)
- [Linux 设备树的节点 device_node](./03-驱动开发基础/Linux设备树的节点device_node.md)
- [Linux 驱动核心骨架（总线驱动模型）](./03-驱动开发基础/Linux驱动核心骨架.md)
- [Platform 总线与其他总线的区别](./03-驱动开发基础/Platform总线与其他总线的区别.md)
- [input 子系统](./03-驱动开发基础/input子系统.md)
- [Linux I2C 读写数据的示例](./03-驱动开发基础/linux-i2c读写数据的示例.md)
- [Linux ioctl 操作](./03-驱动开发基础/linux-ioctl操作.md)
- [Linux 串口驱动](./03-驱动开发基础/linux串口驱动.md)
- [Linux 总线驱动模型核心例程](./03-驱动开发基础/linux总线驱动模型核心例程.md)
- [Linux 总线驱动模型设备创建顺序](./03-驱动开发基础/linux总线驱动模型设备创建顺序.md)
- [Linux 时钟](./03-驱动开发基础/linux时钟.md)
- [Linux 驱动设备号](./03-驱动开发基础/linux驱动设备号.md)
- [pinctrl 子系统与 GPIO 子系统](./03-驱动开发基础/pinctrl子系统与GPIO子系统.md)
- [platform 总线](./03-驱动开发基础/platform总线.md)
- [regmap 寄存器访问抽象框架](./03-驱动开发基础/regmap寄存器访问抽象框架.md)
- [regmap 示例](./03-驱动开发基础/regmap示例.md)
- [static 关键字与 const 关键字](./03-驱动开发基础/static关键字与const关键字.md)
- [安装内核模块命令](./03-驱动开发基础/安装内核模块命令.md)
- [注册设备与创建设备的区别](./03-驱动开发基础/注册设备与创建设备的区别.md)
- [设备树的概念](./03-驱动开发基础/设备树的概念.md)
- [设备树解析流程](./03-驱动开发基础/设备树解析流程.md)

### 04-ALSA音频驱动

- [ALSA 学习路线](./04-ALSA音频驱动/ALSA学习路线.md)
- [ALSA 的设备树示例](./04-ALSA音频驱动/ALSA的设备树示例.md)
- [LINUX 开发板录放指令](./04-ALSA音频驱动/LINUX开发板录放指令.md)
- [Machine 驱动（硬件板卡的音频系统配置文件）](./04-ALSA音频驱动/Machine驱动.md)
- [Linux 声卡 ALSA](./04-ALSA音频驱动/linux声卡-ALSA.md)
- [Linux 音频栈](./04-ALSA音频驱动/linux音频栈.md)
- [Linux 音频驱动编译调试流程（ALSA 编译调试）](./04-ALSA音频驱动/linux音频驱动编译调试流程.md)
- [音频数据结构层次](./04-ALSA音频驱动/音频数据结构层次.md)

### 05-编译与构建系统

- [Git 使用方法](./05-编译与构建系统/Git使用方法.md)
- [Kconfig 讲解](./05-编译与构建系统/Kconfig讲解.md)
- [RK3568 编译 Linux 内核 / 驱动模块 / 应用](./05-编译与构建系统/RK3568编译-linux内核-驱动模块-应用.md)
- [Source Insight 使用方法](./05-编译与构建系统/Source-Insight使用方法.md)
- [i.MX6ULL 编译 Linux 内核 / 驱动模块 / 应用](./05-编译与构建系统/i.MX6ULL编译-linux内核-驱动模块-应用.md)
- [imx6ull Linux 驱动 Makefile 模板](./05-编译与构建系统/imx6ull-linux驱动makefile模板.md)
- [imx6ull 芯片内核编译](./05-编译与构建系统/imx6ull芯片内核编译.md)
- [Linux 源码顶层结构](./05-编译与构建系统/linux源码顶层结构.md)
- [Linux 驱动编译流程](./05-编译与构建系统/linux驱动编译流程.md)
- [嵌入式 Linux 编译工具链的不同](./05-编译与构建系统/嵌入式Linux编译工具链的不同.md)
- [编译 imx6ull Linux 应用 app](./05-编译与构建系统/编译imx6ull-linux应用app.md)
- [编译设备树](./05-编译与构建系统/编译设备树.md)

### 06-U-Boot与启动

- [Secure Boot 的核心思想](./06-U-Boot与启动/Secure-Boot-的核心思想.md)
- [U-Boot 启动 Linux 内核指令](./06-U-Boot与启动/uboot启动linux内核指令.md)

### 07-开发板操作与环境

- [LINUX 开发板中 F4 或其他按键失效](./07-开发板操作与环境/LINUX开发板中F4或其他按键失效.md)
- [RK3568 源码结构](./07-开发板操作与环境/RK3568源码结构.md)
- [Linux 备份 eMMC 镜像](./07-开发板操作与环境/linux备份emmc镜像.md)
- [Linux 对内存卡做镜像](./07-开发板操作与环境/linux对内存卡做镜像.md)
- [Linux 开发板 SCP 传输文件](./07-开发板操作与环境/linux开发板scp传输文件.md)
- [Linux 开发板常用命令](./07-开发板操作与环境/linux开发板常用命令.md)
- [Linux 开发板挂载共享文件夹](./07-开发板操作与环境/linux开发板挂载共享文件夹.md)
- [Linux 开发板查看 CPU 温度](./07-开发板操作与环境/linux开发板查看CPU温度.md)
- [Linux 开发板查看系统信息](./07-开发板操作与环境/linux开发板查看系统信息.md)
- [Linux 开发板设置静态 IP](./07-开发板操作与环境/linux开发板设置静态IP.md)
- [Linux 文件目录](./07-开发板操作与环境/linux文件目录.md)
- [挂载 U 盘](./07-开发板操作与环境/挂载U盘.md)

### 08-C语言与软件设计

- [C语言常见问题](./08-C语言与软件设计/C语言常见问题.md)
- [低性能MCU软件设计分层](./08-C语言与软件设计/低性能MCU软件设计分层.md)

### 09-图形系统

- [LINUX图形系统本质](./09-图形系统/LINUX图形系统本质.md)
- [图形界面QT等](./09-图形系统/图形界面QT等.md)

### 10-其他

- [yml文件讲解](./10-其他/yml文件讲解.md)
- [智能体运行方式](./10-其他/智能体运行方式.md)
<!-- TOC END -->

---

## 📝 说明

- 本笔记基于学习过程整理，内容可能存在不准确之处，欢迎指正
- 代码示例主要基于 Linux Kernel 4.19，适用于 ARM 架构嵌入式平台
- 图片资源存放在 `images/` 目录下
