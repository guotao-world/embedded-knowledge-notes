# uboot启动linux内核指令

**uboot启动linux内核指令1：**

fatload mmc 0:1 0x82000000 zImage
fatload mmc 0:1 0x83000000 rk3568.dtb
setenv bootargs console=ttyFIQ0,1500000 root=/dev/mmcblk2p2 rw
bootz 0x82000000 - 0x83000000

**uboot启动linux内核指令2：**

fatload mmc 0:1 0x82000000 boot.itb
bootm 0x82000000

**基本语法**：

fatload <interface> <dev[:part]> <addr> <filename> [bytes]

<interface>：接口

**命令启动格式：**

bootz： zImage
booti： Image
bootm： uImage/FIT

**fatload 的固定语法是：**

fatload <接口> <设备:分区> <内存地址> <文件名>

· 第1个参数：接口（如 mmc、usb、sata）

· 第2个参数：设备号和分区（如 0:1）

· 第3个参数：加载的内存地址（如 0x82000000）

· 第4个参数：文件名（如 zImage）

**设计思想：**

· 第一步：告诉 CPU "我要操作哪个硬件"（mmc 0:1）------先接通链路；

· 第二步：告诉 CPU "把数据暂存到哪个门牌号"（0x82000000）------先分配好篮子；

· 第三步：告诉 CPU "去把那个叫 zImage 的东西搬进来" ------最后动手干活。

** bootcmd（启动命令）------ 给 U-Boot 看的"自动执行清单"，它是一个命令列表，U-Boot 开机倒计时结束后会自动执行里面的命令：**

setenv bootcmd 'fatload mmc 0:1 0x82000000 zImage; fatload mmc 0:1 0x83000000 rk3568.dtb; bootz 0x82000000 - 0x83000000'
saveenv

**bootz与boot区别**：

bootz zImage ARM32（常见） 压缩
booti Image ARM64（常见）通常不压缩

**注意：**

**内核启动后printk调用流程**

start_kernel
   ↓
setup_arch
   ↓parse_early_param   ↓earlycon init  ← 可最早打印   ↓driver initcalls   ↓platform_driver probe(UART)   ↓register_console(normal)   ↓完整 printk console   ↓tty/getty**console=ttyS0表示**：输出：printk内核日志默认发往 ttyS0输入/输出：/dev/console 默认绑定 ttyS0register_console(...)给内核日志系统（printk）注册"日志输出口"tty_register_driver(...)给 tty 子系统注册"终端设备类型"