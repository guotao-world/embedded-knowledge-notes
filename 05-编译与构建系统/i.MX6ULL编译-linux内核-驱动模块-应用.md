# i.MX6ULL 编译 Linux 内核 / 驱动模块 / 应用

## 一、编码约定

在 Linux 下（包括内核、工具链、脚本系统）：

```
默认约定：UTF-8 = 无 BOM
```

i.MX6ULL 当前内核版本：**4.1.15**

---

## 二、设置交叉编译器

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
```

---

## 三、Ubuntu 编译内核

### 内核配置准备

如果你有 `.config`（BSP 或上次编译生成的配置），它会：

- 检查 `.config` 是否完整
- 生成模块编译需要的头文件

如果没有 `.config`，可以用 `defconfig` 生成默认配置：

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
```

然后准备头文件和模块环境：

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- prepare
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules_prepare
make -j16
```

---

## 四、IP 配置

### Ubuntu IP 配置

```bash
sudo ifconfig ens33 192.168.55.72 netmask 255.255.255.0
route add default gw 192.168.55.1
```

### 开发板 IP 配置

```bash
# 需要两个命令
sudo ifconfig eth1 192.168.55.71 netmask 255.255.255.0
route add default gw 192.168.55.1

# 查看也需要两个命令
ifconfig eth1
route -n
```

---

## 五、IP 配置加入开机自启动

### Ubuntu 16

```bash
sudo vi /etc/network/interfaces
```

后面加入：

```
auto ens33
iface ens33 inet static
    address 192.168.55.72
    netmask 255.255.255.0
    gateway 192.168.55.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

随后重新加载配置：

```bash
ifdown eth33 && ifup eth33
```

### SSH

```bash
sudo service ssh start
sudo service ssh status
```

### Linux 开发板

**方法 1**（有时候错误太多）：

```bash
sudo vi /etc/network/interfaces
```

后面加入：

```
auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet static
        address 192.168.55.71
        netmask 255.255.255.0
        gateway 192.168.55.1
        dns-nameservers 8.8.8.8 8.8.4.4
```

随后重新加载配置：

```bash
ifdown eth1 && ifup eth1
```

**方法 2**（用这个虽然不规范，但是很方便）：

操作这个文件：

```bash
vi /etc/rc.local
```

按照下列示例修改：

```sh
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

echo 30000 >  /proc/sys/vm/min_free_kbytes
source /etc/profile
/opt/QDesktop >/dev/null 2>&1 &

# set eth1 ip
/sbin/ifconfig eth1 192.168.55.71 netmask 255.255.255.0 up
/sbin/route add default gw 192.168.55.1 dev eth1

exit 0
```

### 测试网络

```bash
ping 192.168.55.69
```

---

## 六、从 Linux 开发板获取内核配置

### 确认内核版本和架构

```bash
uname -r    # 版本示例：4.1.15-g3dc0a4b
uname -m    # 架构示例：armv7l（IMX6ULL）
```

### 尝试获取内核配置

```bash
# 通常在 /proc/config.gz
zcat /proc/config.gz > ~/board_kernel.config
```

如果 `/proc/config.gz` 不存在：

```bash
# 从内核镜像中提取
strings /boot/vmlinuz-$(uname -r) | grep CONFIG_ > ~/board_kernel.config
```

将 `board_kernel.config` 复制到宿主机（通过 NFS、scp、U 盘等方式）。

---

## 七、准备内核源码并编译

设置交叉编译器：

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
```

### 准备内核源码

下载或者使用 BSP 提供的与板子内核版本尽量一致的源码。

假设源码目录为 `/home/zhangxin/linuxShare/IMX6ULL/linux-source`。

### 应用开发板配置

```bash
cd /home/zhangxin/linuxShare/IMX6ULL/linux-source
cp ~/board_kernel.config .config
make ARCH=arm CROSS_COMPILE=$CROSS_COMPILE oldconfig
make ARCH=arm CROSS_COMPILE=$CROSS_COMPILE prepare
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules_prepare
```

说明：

- `oldconfig` 会根据 `.config` 更新内核源码配置
- `prepare` 会生成模块编译所需的头文件和 Makefile

需要继续更改模块配置时：

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```

### 编译

```bash
make -j16
```

### 内核在源码中的位置

```
kernel/arch/arm/boot/zImage
```

用的内核压缩包：

```
linux-imx-4.1.15-2.1.0-gad512fa-v1.7.tar.bz2
```

---

## 八、i.MX6ULL Linux 驱动 Makefile 模板

```makefile
# 内核源码路径
KERNELDIR := /home/zhangxin/workspace_imx6ull/kernel

# 当前模块源码路径
CURRENT_PATH := $(shell pwd)

# 交叉编译器前缀（根据你实际工具链修改）
CROSS_COMPILE := arm-linux-gnueabihf-
ARCH := arm

# 模块列表
obj-m := led.o

# 默认目标
all: build

# 编译模块
build: kernel_modules

kernel_modules:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

# 清理模块
clean:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) clean
```

---

## 九、编译 i.MX6ULL Linux 应用 APP

### 环境安装

**1. 下载**

去 Linaro 官网下载适合 64 位系统的版本，比如：

```
gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz
```

**2. 解压**（假设放到 `/usr/local/arm`）：

```bash
sudo mkdir -p /usr/local/arm
sudo tar -xvf gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz -C /usr/local/arm/
```

**3. 配置并验证环境变量**

为了让编译器随时可用，将 `bin` 目录加入环境变量：

```bash
export PATH=$PATH:/usr/local/arm/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf/bin
```

永久加入环境变量（为了省事可以加入 `/etc/profile`）：

- `~/.bashrc`（用户级）
- `~/.profile` 或 `~/.bash_profile`（用户级登录脚本）
- `/etc/profile` 和 `/etc/environment`（系统级全局配置）

> AI 建议：不要动 `~/.profile`（因为它是系统级敏感配置，容易影响桌面环境）。直接在 `~/.bashrc` 末尾添加（最稳妥，只影响终端）。

**4. 生效并验证**：

```bash
arm-linux-gnueabihf-gcc -v
```

**5. 若使用 Makefile 则需**：

```bash
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export PATH=$PATH:/your/toolchain/bin
```

### 编译 APP 标准指令

```bash
${CC} -o testApp testApp.c -Ixxx -Lyyy -lzzz
```

- `xxx` 表示头文件的路径
- `yyy` 表示库文件的路径
- `zzz` 表示链接库

### 编译示例

```bash
arm-linux-gnueabihf-gcc hello.c -o hello

arm-linux-gnueabihf-gcc -std=gnu99 \
  --sysroot=/opt/fsl-imx-x11/4.1.15-2.1.0/sysroots/cortexa7hf-neon-poky-linux-gnueabi \
  -o playAndRecoed playAndRecoed.c -lpthread -lasound
```

### 使用 SSH 拷贝到开发板

```bash
scp helloworld root@192.168.55.71:/home/root/
scp audioApp root@192.168.55.71:/home/root/
scp playAndRecoed root@192.168.55.71:/home/root/
```

### 在开发板上执行

```bash
chmod +x audioApp
./audioApp
```

### 验证文件架构

使用 `file` 命令查看文件属性，确认它确实是 ARM 架构的：

```bash
file helloworld
```
