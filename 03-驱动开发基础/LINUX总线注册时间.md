# LINUX 总线注册时间

## 一、Linux 内核的实际模型（以 SPI 总线为例）

```
Driver Model
      │
┌─────┴───────────────┐
│                     │
Platform Bus      SPI Bus (spi_bus_type)
      │                     │
      │           ├── spi_device(flash)
      │           ├── spi_device(codec)
      │           └── spi_driver(...)
      │
├── platform_device(ecspi1)
│         │
│         └──── probe(spi-imx)
│                   │
│                   ▼
│             spi_controller
│                   │
│                   └── 管理整个 SPI Bus 上属于自己的所有 spi_device
│
└── platform_driver(spi-imx)
```

## 二、四个概念的注册时机

**SPI 总线（spi_bus_type）不是在 SPI 控制器（SPI Master/Controller）probe 时注册的。**

需要把几个概念区分开：

| 概念 | 说明 |
|------|------|
| bus | 总线类型 |
| controller | SPI 控制器 |
| device | SPI 设备 |
| driver | SPI 驱动 |

它们注册的时机完全不同。

### 1. bus 是什么时候注册的？

`spi_bus_type` 只是 SPI Core 管理的一部分。SPI 总线是在 SPI 子系统初始化的时候注册的。

Linux 内核启动过程中，大概顺序是：

```
start_kernel()
    ↓
do_basic_setup()
    ↓
driver_init()
    ↓
do_initcalls()
    ↓
SPI 子系统（spi.c）的 init 函数
```

例如（4.x 内核）：

```c
static int __init spi_init(void)
{
    bus_register(&spi_bus_type);
    class_register(&spi_master_class);
    ...
}
subsys_initcall(spi_init);
```

### 2. 为什么这么早注册？

因为 Driver Model 要先知道世界上有一种 bus 叫 SPI，以后任何 `spi_device`、`spi_driver` 才能往这个 bus 上挂。

就像：

```
bus_register()
    ↓
创建了一块停车场
    ↓
以后才能停车
```
