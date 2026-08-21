# paltform总线

**定义：**

```c
struct bus_type platform_bus_type = {
.name = "platform",
.match = platform_match,
.uevent = platform_uevent,
.pm = &platform_dev_pm_ops,
};
struct bus_type spi_bus_type = {
.name= "spi",
.dev_groups= spi_dev_groups,
.match= spi_match_device,
.uevent= spi_uevent,
};
```

**paltform总线注册顺序：**

**1. platform_bus_type 注册（早期）**

**2. DT 被解析成 device_node（unflatten）**

**3. of_platform_populate() 被调用（arch_initcall）**

**4. platform_device 被创建（platform_device 不是通过 bus 去发现的，而是：DT / ACPI → 主动创建）**

**5. platform_driver 开始 match + probe**

**paltform总线与其他总线设备创建的区别：**

platform bus 设备先由系统/DT创建，再交给 bus 做 match。

其他bus设备是由相应的bus控制器/枚举器创建，再交给 bus 做 match。