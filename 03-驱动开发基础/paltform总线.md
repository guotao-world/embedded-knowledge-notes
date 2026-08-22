# platform 总线

## 一、总线定义

```c
struct bus_type platform_bus_type = {
    .name   = "platform",
    .match  = platform_match,
    .uevent = platform_uevent,
    .pm     = &platform_dev_pm_ops,
};

struct bus_type spi_bus_type = {
    .name       = "spi",
    .dev_groups = spi_dev_groups,
    .match      = spi_match_device,
    .uevent     = spi_uevent,
};
```

---

## 二、platform 总线注册顺序

```
1. platform_bus_type 注册（早期）
2. DT 被解析成 device_node（unflatten）
3. of_platform_populate() 被调用（arch_initcall）
4. platform_device 被创建
   （platform_device 不是通过 bus 去发现的，而是：DT / ACPI → 主动创建）
5. platform_driver 开始 match + probe
```

---

## 三、platform 总线与其他总线设备创建的区别

| 总线类型 | 设备创建方式 |
|---------|------------|
| **platform bus** | 设备先由系统/DT 创建，再交给 bus 做 match |
| **其他 bus（I2C/SPI/PCI等）** | 设备由相应的 bus 控制器/枚举器创建，再交给 bus 做 match |

> platform 设备是"静态描述、主动创建"的，因为 SoC 内部外设无法被硬件自动枚举，必须通过设备树或板级代码提前告知内核。
