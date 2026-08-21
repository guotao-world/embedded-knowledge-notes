<<<<<<< HEAD
# 嵌入式 Linux 常用命令
=======
# 嵌入式 Linux 基础命令
>>>>>>> 8d2bfbc45cf20452045f5bb8536863761812c93a

> 面向嵌入式 Linux 开发、驱动调试、板卡调试、系统维护。

---

# 目录

* 文件系统操作
* 文件查看
* 权限管理
* 进程管理
* 系统信息
* 网络调试
* 串口调试
* USB调试
* 存储管理
* 内核调试
* 设备树
* 驱动模块
* 字符设备
* GPIO
* I2C
* SPI
* ALSA音频
* 调试工具

---

# 1. 文件系统操作

## 当前路径

```bash
pwd
```

## 查看目录

```bash
ls
ls -l
ls -al
```

## 切换目录

```bash
cd /path
cd ..
cd ~
```

## 创建目录

```bash
mkdir test
mkdir -p /home/test
```

## 删除

```bash
rm file
rm -rf dir
```

## 复制

```bash
cp file1 file2
cp -r dir1 dir2
```

## 移动

```bash
mv old new
```

---

# 2. 文件查看

## 查看文件

```bash
cat file
```

分页：

```bash
less file
```

查看前面：

```bash
head -n 20 file
```

查看末尾：

```bash
tail -n 20 file
```

实时查看日志：

```bash
tail -f log
```

---

# 3. 文件搜索

搜索内容：

```bash
grep "text" file
```

递归搜索：

```bash
grep -r "text" .
```

查找文件：

```bash
find / -name "*.ko"
```

---

# 4. 权限管理

查看权限：

```bash
ls -l
```

修改权限：

```bash
chmod 755 app
chmod +x app
```

修改用户：

```bash
chown root:root file
```

权限含义：

```
r 读
w 写
x 执行
```

---

# 5. 进程管理

查看进程：

```bash
ps
ps -ef
```

动态查看：

```bash
top
```

结束进程：

```bash
kill PID
kill -9 PID
```

后台运行：

```bash
./app &
```

---

# 6. CPU和内存

CPU信息：

```bash
cat /proc/cpuinfo
```

内核版本：

```bash
uname -a
uname -r
```

内存：

```bash
free -h
```

系统信息：

```bash
cat /proc/version
```

---

# 7. 网络调试

查看IP：

```bash
ifconfig
```

或者：

```bash
ip addr
```

查看网卡：

```bash
ip link
```

测试网络：

```bash
ping 192.168.1.1
```

查看路由：

```bash
ip route
```

SSH：

```bash
ssh root@192.168.1.100
```

文件传输：

```bash
scp file root@ip:/path
```

---

# 8. 串口调试

查看串口：

```bash
ls /dev/tty*
```

常见：

```
/dev/ttyS0
/dev/ttyUSB0
/dev/ttyACM0
```

minicom：

```bash
minicom -D /dev/ttyUSB0 -b 115200
```

screen：

```bash
screen /dev/ttyUSB0 115200
```

---

# 9. USB调试

查看USB：

```bash
lsusb
```

查看USB日志：

```bash
dmesg | grep usb
```

---

# 10. 存储管理

查看挂载：

```bash
mount
```

查看空间：

```bash
df -h
```

查看块设备：

```bash
lsblk
```

挂载：

```bash
mount /dev/sda1 /mnt
```

卸载：

```bash
umount /mnt
```

---

# 11. 内核调试

查看内核日志：

```bash
dmesg
```

实时：

```bash
dmesg -w
```

过滤：

```bash
dmesg | grep driver
```

查看启动信息：

```bash
dmesg | less
```

---

# 12. 设备树查看

设备树目录：

```bash
ls /proc/device-tree
```

查看model：

```bash
cat /proc/device-tree/model
```

查看节点：

```bash
ls /proc/device-tree/
```

---

# 13. 驱动模块

查看模块：

```bash
lsmod
```

加载：

```bash
insmod xxx.ko
```

卸载：

````bash
rmmod xxx
````

构建依赖数据库：

```bash
depmod
````

加载模块：

```bash
modprobe xxx
````

查看模块信息：

```bash
modinfo xxx.ko
```

```
```

---

# 14. 字符设备

查看设备：

```bash
ls /dev
```

查看设备号：

```bash
cat /proc/devices
```

创建节点：

```bash
mknod /dev/test c 200 0
```

格式：

```
mknod 文件 类型 主设备号 次设备号
```

---

# 15. GPIO调试

查看GPIO：

```bash
cat /sys/kernel/debug/gpio
```

sysfs GPIO：

导出：

```bash
echo 20 > /sys/class/gpio/export
```

设置方向：

```bash
echo out > /sys/class/gpio/gpio20/direction
```

输出：

```bash
echo 1 > /sys/class/gpio/gpio20/value
```

---

# 16. I2C调试

安装：

```bash
apt install i2c-tools
```

查看总线：

```bash
i2cdetect -l
```

扫描设备：

```bash
i2cdetect -y 1
```

读寄存器：

```bash
i2cget -y 1 0x50 0x00
```

写寄存器：

```bash
i2cset -y 1 0x50 0x00 0xff
```

---

# 17. SPI调试

查看SPI设备：

```bash
ls /dev/spidev*
```

查看日志：

```bash
dmesg | grep spi
```

---

# 18. ALSA音频调试

查看播放设备：

```bash
aplay -l
```

查看录音设备：

```bash
arecord -l
```

播放：

```bash
aplay test.wav
```

录音：

```bash
arecord -d 5 test.wav
```

查看声卡：

```bash
cat /proc/asound/cards
```

---

# 19. 调试工具

查看系统调用：

```bash
strace ./app
```

查看动态库：

```bash
ldd app
```

查看文件类型：

```bash
file app
```

查看符号：

```bash
nm app
```

十六进制查看：

```bash
hexdump -C file
```

---

# 20. 嵌入式常用调试组合

## 查看驱动是否加载

```bash
lsmod
dmesg | tail
```

## 查看设备是否注册

```bash
cat /proc/devices
ls /dev
```

## 查看GPIO问题

```bash
cat /sys/kernel/debug/gpio
dmesg | grep gpio
```

## 查看I2C问题

```bash
i2cdetect -y 1
dmesg | grep i2c
```

## 查看音频问题

```bash
aplay -l
arecord -l
dmesg | grep snd
```

---

# 常用目录说明

```
/proc
    内核运行状态

/sys
    Linux设备模型

/dev
    设备节点

/lib/modules
    内核模块

/etc
    系统配置

/tmp
    临时文件

/mnt
    挂载目录
```

---

# 嵌入式Linux调试核心命令

```
dmesg
    查看内核日志

lsmod
    查看驱动模块

insmod
    加载驱动

rmmod
    卸载驱动

cat /proc
    查看内核信息

cat /sys
    查看设备信息

ls /dev
    查看设备节点
```
