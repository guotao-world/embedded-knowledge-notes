# linux驱动设备号

**行为（ops）**是"驱动级"

**设备（cdev）**是"实例级"

多个设备号 → 可以映射到同一个 cdev → 这个 cdev 绑定一个 ops

**Q:register_chrdev相当于cdev+register_chrdev_region吗？**

**A：简化模型如下：**

register_chrdev()
↓
__register_chrdev()
├── alloc_chrdev_region() / register_chrdev_region()
│ ↓
│ 申请设备号
│
├── cdev_init()
│ ↓
│ 初始化 cdev
│
└── cdev_add()
↓
注册 cdev

**Q:为什么必须创建类以后才能device_create？**

**A:**device_create() 创建的并不只是你看到的 /dev/led 这个文件，它本质上是在 Linux**设备模型（driver model）里创建一个 struct device，而 class 是这个 device 在设备模型中的归属层级/容器**
。device_create()是 Linux**设备模型**中的操作,**如果你想使用 device_create() 来让 Linux 设备模型创建/管理这个设备，那么必须先有一个 struct class**，因为 device_create() 要把新建的 struct device 挂到这个 class 下。

**Q：为什么要设置私有数据？如open的时候进行filp->private_data = &testdev;**

**A:**在open函数里面设置好私有数据以后，在write、read、close等函数中直接读取private_data即可得到设备结构体。