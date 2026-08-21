# linux ioctl操作

**ioctl命令：**

```c
#define LED_MAGIC 'L'
#define LED_ON _IO(LED_MAGIC,1)
```

**含义：**

设备类型=L

命令编号=1

无参数

**参数区别：**

_IO 无参数 开灯

_IOW 用户传给内核 设置亮度

_IOR 内核返回用户 读取温度

_IOWR 双向 配置并返回结果

**unlocked_ioctl：**

不是"不加锁"，而是：

内核不再自动加旧的大内核锁，驱动需要自己保证并发安全。

**Q: 这个magic必须是L？**

**A: 不必须是 'L'。LED_MAGIC可以是任意一个合适的值，**'L' 只是一个人为约定，用来表示"这是 LED 设备的 ioctl 命令"**。**

**注意：magic不是固定值，但是内核驱动和用户程序必须使用同一个 magic 定义。**magic 主要是为了保证 ioctl 接口（用户空间 ABI）的命名和管理不混乱，而不是为了防止内核根据 ioctl 找错设备。