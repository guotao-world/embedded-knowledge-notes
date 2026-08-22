# Linux 驱动编译流程

## 一、设置交叉编译器

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
```

## 二、编译驱动

```bash
make
```

## 三、编译测试程序

```bash
arm-linux-gnueabihf-gcc ledApp.c -o ledApp
```

## 四、列出当前驱动

```bash
lsmod
```

## 五、改变 LED 的触发模式

```bash
echo none > /sys/class/leds/sys-led/trigger
```

## 六、打印调试信息环形缓冲区的最后几条

```bash
dmesg | tail -n 20
```

## 七、临时调试命令

```bash
ls /proc/device-tree/beep/
insmod beep.ko
dmesg | tail -n 5
```
