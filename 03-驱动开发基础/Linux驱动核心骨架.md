# Linux驱动核心骨架（总线驱动模型）

**"统一接口 + 私有扩展"架构**

1️⃣ driver core（统一规则）
    - device
    - driver
    - bus
    - match / probe
2️⃣ 各种子系统（SPI / I2C / platform）
    - 定义自己的 device / driver
    - 复用 driver core
3️⃣ controller（硬件入口）
    - 真正操作寄存器 / DMA / 中断
4️⃣ 具体设备驱动
    - 业务逻辑（sensor / flash / lcd）

**备注：**

-   **bus 只是定义了一套规则。match() 是 Bus 制定的"游戏规则"，match 是 Bus 提供的服务。**

**不是 Driver。bus 可以有自己的 probe，但是platdorm没有、spi也没有，只有极少数特殊总线才会覆盖 bus->probe。**

-   **SPI Bus 属于 SPI Core。**或者说：**SPI Core 包含了 SPI Bus。**

**SPI Core**

│

├── spi_bus_type

├── spi_register_controller()

├── spi_unregister_controller()

├── spi_add_device()

├── spi_register_driver()

├── spi_match_device()

├── spi_sync()

├── spi_async()

└── ...

-   **SPI 为什么一个叫 register，一个叫 add？**因为它们代表两种完全不同的生命周期： **spi_device 是由其他对象"拥有（owned）"的，所以叫 add_device()；spi_driver 是向总线"声明自己"的，所以叫 register_driver()。**这两个名字并不是随便起的，而是反映了它们的生命周期。另外就是驱动是主动注册的的、设备是被驱动添加的

-   **DTS 只存"静态常量"，驱动做"动态操作"**。这是 Linux 内核几十年演进下来的最稳健的工程实践，所以probe函数放到驱动里，devices不做初始化。

-   **driver core 只处理通用的 struct device 抽象**，不关心子系统的扩展字段，这些字段由各子系统（如 SPI）在 probe 之后使用。

-   struct device 不是"全部信息"，而是所有设备的最小公共集合（common denominator），其他信息是按子系统分层扩展的，而不是冗余。

if (sdrv->probe)sdrv->driver.probe = spi_drv_probe;这句的本质： 把 driver core 要调用的 probe，换成了 SPI 自己的函数**在驱动注册时进行匹配**，匹配成功后调用probe函数，在之后才会进行创建/sys节点文件等操作，核心函数为**__driver_attach，**核心语句为**dev->driver = drv;**。**pinctrl_bind_pins(dev) 也在__driver_attach函**数种，的作用是：在驱动 probe 之前，把设备的硬件引脚复用关系配置正确，确保外设通信链路是可用的。所以说，**在驱动注册的过程中，一旦通过compatible匹配好了设备，就会先调用pintrl子系统初始化好pin复用，之后再进行probe。内核是怎么匹配的？（匹配顺序）**内核在遍历匹配时，遵循**"设备树优先，驱动表内按序"**的规则。伪代码逻辑如下：取出设备树compatible属性里的**第 1 个**字符串（最具体的）。拿着这个字符串，去驱动表imx_uart_dt_ids里**从头到尾**（按数组顺序）找有没有一样的。如果找到，匹配成功，立即停止，**不再往下看**。如果第 1 个没找到，再取设备树的**第 2 个**字符串，重复上述步骤。**内核在遍历匹配时，遵循"设备树优先，驱动表内按序"的规则。**

**linux内核代码特点：**Linux 倾向"函数短 + 调用链深"，是为了在复杂系统里获得更好的可维护性、解耦和可演进性。