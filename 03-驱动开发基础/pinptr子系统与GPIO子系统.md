# pinptr子系统与GPIO子系统

**IO结构：**

物理 Pin(封装引出的管脚)

│

│

Pad IO电气单元在（pad包括Pin Mux ）

pinctrl 配置 Pin Mux + PAD 电气属性

│

+-------------------+

│ │

GPIO功能 外设功能

│ │

gpio_chip UART/SPI/SAI/I2C Controller

│

GPIO Framework

**pin与pad的区别：**

**Pin 是芯片封装出来的外部引脚；Pad 是芯片内部连接这个引脚的 IO 电路单元。一个 Pin 背后通常对应一个 Pad，Pad 决定这个 Pin 的电气属性和复用功能。**

**pinptr子系统的实现：**

pinctrl 核心（通用框架）

        ↓

根据 compatible 匹配

        ↓

加载 SoC 专用 pinctrl 驱动（如 pinctrl-imx）

        ↓

由这个驱动去解析 fsl,pins（私有格式）

**Linux pinctrl 是三步模型(pinctrl_bind_pins)：**

get      → 获取所有状态集合

lookup   → 找某个状态对象

select   → 真正配置硬件 IO

**最终的配置是在这个函数：**

pinctrl_bind_pins

        ↓

pinmux_enable_setting

        ↓

ops->set_mux

        ↓imx_pmx_set

**笔记：DTS 中 &xxx 引用的优先级是：首先查找节点标签（label）**，即你在 DTS 中直接写的 gpio4: 标签如果节点标签找不到，再查 /aliases 中是否有对应的别名

**SNVS：**Secure Non-Volatile Storage**gpiod：**d = descriptor（描述符）

**宏：u32 pins[] = {    mux_reg, mux_val, input_reg, input_val, config_reg, pad_ctrl};for (...) {    mux_reg   = vals[i++];    mux_mode  = vals[i++];    input_reg = vals[i++];    input_val = vals[i++];    config    = vals[i++];    pad_ctrl  = vals[i++];}在 pinctrl 驱动里：writel(mux_mode, base + mux_reg);本质就是：*(mux寄存器) = mux_mode;**

**注意：**因为 input_reg 不是"每个 pin 固有的属性"，而是"和具体复用功能相关"的属性，所以不放在** imx_pin**里面。**groups ------ 设备树解析结果：**structimx_pin_group*groups;unsignedintngroups;**mux_reg / conf_reg 是"物理引脚属性"input_reg / input_val 是"信号路径选择属性"**struct** imx_pin_reg** {    s16 mux_reg;    s16 conf_reg;};struct** imx_pin** {    unsigned int pin;    unsigned int mux_mode;    u16 input_reg;    unsigned int input_val;    unsigned long config;};struct** imx_pin_group** {    const char *name;    unsigned npins;    unsigned int *pin_ids;    struct imx_pin *pins;};

**pinctrl-names：**状态名字 pinctrl-names = "default", "sleep";多个状态时→ pinctrl-names 必须写，否则驱动无法按名字查找

**pinctrl-0：**0 是"第0个 pinctrl 状态"的索引（index）**pinctrl-1：**1 是"第0个 pinctrl 状态"的索引（index）例如：pinctrl-names = "default", "sleep";pinctrl-0 = <&pinctrl_led>;pinctrl-1 = <&pinctrl_led_sleep>;

**为什么要设计成数组：**因为一个设备可能有多个状态：default（正常工作）sleep（低功耗）idle（空闲）切换时可以 pinctrl_select_state(...)

**关于GPIO_ACTIVE_HIGH逻辑激活方式：**驱动只用 gpiod_set_value(desc, 1) / 0GPIO_ACTIVE_HIGH → 1 就输出高电平，0 输出低电平GPIO_ACTIVE_LOW → 1 就输出低电平，0 输出高电平在使用 gpiod API 时，它可以让驱动不用关心电平翻转问题：gpiod_set_value(desc,1);// LED 总是亮，不管硬件是高激活还是低激活

**注册顺序：**1、insmod → 注册 platform_driver2、内核会根据：**compatible = "atkalpha-led";**匹配驱动：.of_match_table=...3、驱动一进 probe，就已经知道自己对应哪个设备树节点了

**写法：**pinctrl_led: ledgrp {    fsl,pins = <        MX6ULL_PAD_GPIO1_IO03__GPIO1_IO03 0x10B0    >;};

led {
    compatible = "atkalpha-led";

    pinctrl-names = "default";    pinctrl-0 = <&pinctrl_led>;

    led-gpios = <&gpio1 3 GPIO_ACTIVE_HIGH>;};

desc = gpiod_get(dev, "led", GPIOD_OUT_LOW);gpiod_set_value(desc, 1);

**流程：**设备树    ↓led-gpios = <&gpio1 3 ...>    ↓gpiod_get("led")    ↓of_get_named_gpiod_flags()    ↓找到 gpio1（gpiochip）    ↓创建 gpio_desc（第3个引脚）    ↓gpiod_direction_output()    ↓gpio_chip->direction_output()    ↓写 GDIR 寄存器    ↓gpiod_set_value()    ↓gpio_chip->set()    ↓写 DR 寄存器

备注：芯片在上电后、内核软件初始化之前，所有GPIO会进入一个确定的、安全的状态。这个状态通常在芯片数据手册的"GPIO章节"或"系统复位与控制章节"有明确说明。主要有以下两种安全机制：· 默认高阻态（Hi-Z）：大多数IO口复位后默认为高阻态的输入模式。相当于引脚内部和电路断开了，电平由外部电路决定。这能极大避免短路，因为高阻态下引脚不会主动输出高或低电平来对抗外部电路。· 默认内部上下拉：部分关键引脚（如启动配置脚、调试接口）在复位后会有确定的内部弱上拉或下拉，确保其在软件配置前有确定的逻辑电平。