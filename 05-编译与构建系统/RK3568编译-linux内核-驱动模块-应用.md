# RK3568 编译 Linux 内核 / 驱动模块 / 应用

## 一、关闭开发板心跳灯

```bash
echo none > /sys/class/leds/work/trigger
```

---

## 二、编译内核镜像

### 使用的配置文件

```
BoardConfig-rk3568-atk-evb1-ddr4-v10.mk
```

### 编译

进入到顶层目录下，执行命令：

```bash
./build.sh kernel
```

或：

```bash
cd kernel
./make.sh
device/rockchip/common/mk-fitimage.sh kernel/boot.img device/rockchip/rk356x/boot.its
cd ../
```

### 拷贝到开发板

```bash
scp kernel/boot.img root@192.168.55.71:/temp/
```

### 开发板烧写（开发板执行）

```bash
dd if=boot.img of=/dev/mmcblk0p3 status=progress
sync
reboot
```

### 查看开发板分区

| 命令 | 作用 |
|------|------|
| `cat /proc/partitions` | Linux 内核识别出来的块设备和分区大小 |
| `fdisk -l` | 读取 GPT 分区表，显示每个分区的起始位置、结束位置、名字等 |
| `lsblk` | 问内核"你现在管理了哪些块设备？" |
| `df -h` | disk free，查看磁盘文件系统剩余空间；`-h` = human readable |

---

## 三、编译驱动模块

### 修改 Makefile

Makefile 示例：

```makefile
KERNELDIR := /home/alientek/workspace/rk3568_linux_sdk/kernel
CURRENT_PATH := $(shell pwd)
ARCH := arm64
CROSS_COMPILE := ../prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-

obj-m := chrdevbase.o

build: kernel_modules

kernel_modules:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

clean:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) clean
```

### 编译驱动

```bash
make
```

### 拷贝驱动

```bash
scp chrdevbase.ko root@192.168.55.71:/lib/modules/4.19.232/
```

### 安装驱动

```bash
depmod
modprobe chrdevbase
```

### 卸载驱动

```bash
modprobe -r chrdevbase
```

---

## 四、编译应用

### 查看交叉编译器

```bash
ls buildroot/output/rockchip_rk3568/host/usr/bin | grep aarch64
```

### 编译示例

```bash
./../../buildroot/output/rockchip_rk3568/host/usr/bin/aarch64-buildroot-linux-gnu-gcc chrdevbaseApp.c -o chrdevbaseApp
```

### 拷贝 APP

```bash
scp chrdevbaseApp root@192.168.55.71:/temp/
```

---

## 五、注意事项

交叉编译器通常使用构建根文件系统的编译器。有的编译器会自动添加 `sysroot`，添加 `sysroot` 的作用是为了使用开发板里面的根文件系统的 ARM64 库。
