# U-Boot 启动 Linux 内核指令

## 一、启动指令 1（zImage + dtb 分开加载）

```bash
fatload mmc 0:1 0x82000000 zImage
fatload mmc 0:1 0x83000000 rk3568.dtb
setenv bootargs console=ttyFIQ0,1500000 root=/dev/mmcblk2p2 rw
bootz 0x82000000 - 0x83000000
```

## 二、启动指令 2（FIT 镜像）

```bash
fatload mmc 0:1 0x82000000 boot.itb
bootm 0x82000000
```

---

## 三、基本语法

### fatload

```
fatload <interface> <dev[:part]> <addr> <filename> [bytes]
```

| 参数 | 含义 | 示例 |
|------|------|------|
| interface | 接口 | mmc、usb、sata |
| dev[:part] | 设备号和分区 | 0:1 |
| addr | 加载的内存地址 | 0x82000000 |
| filename | 文件名 | zImage |

### 启动命令格式

| 命令 | 镜像类型 | 架构 | 压缩 |
|------|---------|------|------|
| `bootz` | zImage | ARM32（常见） | 压缩 |
| `booti` | Image | ARM64（常见） | 通常不压缩 |
| `bootm` | uImage / FIT | 通用 | 取决于镜像 |

---

## 四、设计思想

1. 第一步：告诉 CPU "我要操作哪个硬件"（mmc 0:1）—— 先接通链路
2. 第二步：告诉 CPU "把数据暂存到哪个门牌号"（0x82000000）—— 先分配好篮子
3. 第三步：告诉 CPU "去把那个叫 zImage 的东西搬进来" —— 最后动手干活

---

## 五、bootcmd（自动启动命令）

`bootcmd` 是给 U-Boot 看的"自动执行清单"，U-Boot 开机倒计时结束后会自动执行里面的命令：

```bash
setenv bootcmd 'fatload mmc 0:1 0x82000000 zImage; fatload mmc 0:1 0x83000000 rk3568.dtb; bootz 0x82000000 - 0x83000000'
saveenv
```

---

## 六、内核启动后 printk 调用流程

```
start_kernel
    ↓
setup_arch
    ↓
parse_early_param
    ↓
earlycon init  ← 可最早打印
    ↓
driver initcalls
    ↓
platform_driver probe (UART)
    ↓
register_console (normal)
    ↓
完整 printk console
    ↓
tty / getty
```

### console=ttyS0 表示

- **输出**：printk 内核日志默认发往 ttyS0
- **输入/输出**：`/dev/console` 默认绑定 ttyS0

### 两个注册的区别

| 函数 | 作用 |
|------|------|
| `register_console(...)` | 给内核日志系统（printk）注册"日志输出口" |
| `tty_register_driver(...)` | 给 tty 子系统注册"终端设备类型" |
