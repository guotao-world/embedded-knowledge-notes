# Linux 总线驱动模型核心例程

## 一、核心结构体

### struct device

```c
struct device {
    struct device *parent;        // 父设备
    struct bus_type *bus;         // 所属总线（SPI / I2C / platform）
    struct device_driver *driver; // 绑定的驱动（匹配成功后才有）
    void *driver_data;            // 私有数据（你常用的）
    struct kobject kobj;          // 内核对象（sysfs）
    ......
};
```

### struct device_driver

```c
struct device_driver {
    const char *name;
    struct bus_type *bus;         // 这个驱动属于哪个总线
    int (*probe)(struct device *dev);
    int (*remove)(struct device *dev);
    ......
};
```

---

## 二、bus（总线）模块

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>

/***********************************************************
 * 函数负责总线下的设备以及驱动匹配
 * 使用字符串比较的方式，通过对比驱动以及设备的名字来确定是否匹配，
 * 如果相同，则说明匹配成功，返回1；反之，则返回0
 ***********************************************************/
int xbus_match(struct device *dev, struct device_driver *drv)
{
    printk("%s-%s\n", __FILE__, __func__);
    if (!strncmp(dev_name(dev), drv->name, strlen(drv->name))) {
        printk("dev & drv match\n");
        return 1;
    }
    return 0;
}

// 定义了一个 bus_name 变量，存放了该总线的名字
static char *bus_name = "xbus";

// 提供 show 回调函数，这样用户便可以通过 cat 命令来查询总线的名称
ssize_t xbus_test_show(struct bus_type *bus, char *buf)
{
    return sprintf(buf, "%s\n", bus_name);
}

// 设置该文件的文件权限为文件拥有者可读，组内成员以及其他所有人不可操作
BUS_ATTR(xbus_test, S_IRUSR, xbus_test_show, NULL);

// 定义了一种新的总线，名为 xbus，总线结构体中最重要的一个成员便是 match 回调函数
static struct bus_type xbus = {
    .name  = "xbus",
    .match = xbus_match,
};
EXPORT_SYMBOL(xbus);

// 注册总线
static __init int xbus_init(void)
{
    printk("xbus init\n");
    bus_register(&xbus);
    bus_create_file(&xbus, &bus_attr_xbus_test);
    return 0;
}
module_init(xbus_init);

// 注销总线
static __exit void xbus_exit(void)
{
    printk("xbus exit\n");
    bus_remove_file(&xbus, &bus_attr_xbus_test);
    bus_unregister(&xbus);
}
module_exit(xbus_exit);

MODULE_AUTHOR("embedfire");
MODULE_LICENSE("GPL");
```

---

## 三、driver（驱动）模块

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>

extern struct bus_type xbus;

char *name = "xdrv";

// 保证 store 和 show 函数的前缀与驱动属性文件一致，drvname_show() 的前缀和 drvname
ssize_t drvname_show(struct device_driver *drv, char *buf)
{
    return sprintf(buf, "%s\n", name);
}

// DRIVER_ATTR_RO 定义了一个 drvname 属性文件
DRIVER_ATTR_RO(drvname);

int xdrv_probe(struct device *dev)
{
    printk("%s-%s\n", __FILE__, __func__);
    return 0;
}

int xdrv_remove(struct device *dev)
{
    printk("%s-%s\n", __FILE__, __func__);
    return 0;
}

// 定义了一个驱动结构体 xdrv，名字需要和设备的名字相同，否则就不能成功匹配
static struct device_driver xdrv = {
    .name   = "xdev",
    // 该驱动挂载在已经注册好的总线 xbus 下
    .bus    = &xbus,
    // 当驱动和设备匹配成功之后，便会执行驱动的 probe 函数
    .probe  = xdrv_probe,
    // 当注销驱动时，需要关闭物理设备的某些功能等
    .remove = xdrv_remove,
};

// 调用 driver_register 函数以及 driver_create_file 函数进行注册我们的驱动以及驱动属性文件
static __init int xdrv_init(void)
{
    printk("xdrv init\n");
    driver_register(&xdrv);
    driver_create_file(&xdrv, &driver_attr_drvname);
    return 0;
}
module_init(xdrv_init);

// 注销驱动以及驱动属性文件
static __exit void xdrv_exit(void)
{
    printk("xdrv exit\n");
    driver_remove_file(&xdrv, &driver_attr_drvname);
    driver_unregister(&xdrv);
}
module_exit(xdrv_exit);

MODULE_AUTHOR("embedfire");
MODULE_LICENSE("GPL");
```

---

## 四、device（设备）模块

```c
#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>

extern struct bus_type xbus;

void xdev_release(struct device *dev)
{
    printk("%s-%s\n", __FILE__, __func__);
}

unsigned long id = 0;

// show 回调函数中，直接将 id 的值通过 sprintf 函数拷贝至 buf 中
ssize_t xdev_id_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    return sprintf(buf, "%d\n", id);
}

/***********************************************************
 * store 回调函数则是利用 kstrtoul 函数，
 * 该函数有三个参数，其中第二个参数是采用几进制的方式，
 * 这里我们传入的是 10，意味着 buf 中的内容将转换为 10 进制的数传递给 id，
 * 实现了通过 sysfs 修改驱动的目的。
 ***********************************************************/
ssize_t xdev_id_store(struct device *dev, struct device_attribute *attr,
                      const char *buf, size_t count)
{
    kstrtoul(buf, 10, &id);
    return count;
}

// DEVICE_ATTR 宏定义定义了 xdev_id，设置该文件的文件权限是文件拥有者可读可写，
// 组内成员以及其他所有人不可操作
DEVICE_ATTR(xdev_id, S_IRUSR | S_IWUSR, xdev_id_show, xdev_id_store);

static struct device xdev = {
    .init_name = "xdev",
    .bus       = &xbus,
    .release   = xdev_release,
};

// 设备结构体以及属性文件结构体注册
static __init int xdev_init(void)
{
    printk("xdev init\n");
    device_register(&xdev);
    device_create_file(&xdev, &dev_attr_xdev_id);
    return 0;
}
module_init(xdev_init);

// 设备结构体以及属性文件结构体注销
static __exit void xdev_exit(void)
{
    printk("xdev exit\n");
    device_remove_file(&xdev, &dev_attr_xdev_id);
    device_unregister(&xdev);
}
module_init(xdev_init);

MODULE_AUTHOR("embedfire");
MODULE_LICENSE("GPL");
```

---

## 五、Makefile

```makefile
KERNEL_DIR = ../ebf-buster-linux/build_image/build
ARCH = arm
CROSS_COMPILE = arm-linux-gnueabihf-
export ARCH CROSS_COMPILE

obj-m := xdev.o xbus.o xdrv.o

all:
	$(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) modules

modules clean:
	$(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) clean
```

---

## 六、加载顺序

```
insmod xbus.ko    # 先注册总线
insmod xdrv.ko    # 再注册驱动
insmod xdev.ko    # 最后注册设备 → 触发 match → probe
```

> 驱动和设备的注册顺序不影响匹配结果，driver core 会在任一方注册时重新遍历匹配。
