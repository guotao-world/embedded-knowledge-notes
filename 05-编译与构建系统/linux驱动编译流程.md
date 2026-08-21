# linux驱动编译流程

**设置交叉编译器：**

export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm

**编译驱动：**

make

**编译测试程序：**

arm-linux-gnueabihf-gcc ledApp.c -o ledApp

**列出当前驱动：**

lsmod

**改变 LED 的触发模式：**

echo none > /sys/class/leds/sys-led/trigger

**打印调试信息环形缓冲区的最后几条：**

dmesg | tail -n 20

**temp：**

ls /proc/device-tree/beep/
insmod beep.ko
dmesg | tail -n 5