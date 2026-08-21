# GPIO子系统描述

**gpio子系统固定写法:**

**< phandle pin flags >**

<&gpio0 RK_PC0 GPIO_ACTIVE_HIGH>

**结构：**

<&gpio0 RK_PC0 GPIO_ACTIVE_HIGH>
│ │ │
│ │ │
│ │ └─ 有效电平
│ └──────────────────── GPIO引脚
└──────────────────────────────── GPIO控制器

**写法：**

**1、of_get_named_gpio(np, "beep-gpios", 0);**

**里面的"0"为index** ------ 第几个 GPIO，这个属性里可能有多个 GPIO，取第几个

led-gpios = <&gpio1 3 GPIO_ACTIVE_HIGH>,
            <&gpio1 4,GPIO_ACTIVE_LOW>;
of_get_named_gpio(np, "led-gpios", 0); // gpio1_3
of_get_named_gpio(np, "led-gpios", 1); // gpio1_4

**2、gpioled.led_gpio=of_get_named_gpio(gpioled.nd,"led-gpio",0);**

<&gpio0 RK_PC0 GPIO_ACTIVE_HIGH>
│
│ 经过 GPIO 控制器解析
▼
Linux GPIO 号
│
▼
gpioled.led_gpio

**3、gpio_request(gpioled.led_gpio, "LED-GPIO");**

第二个参数"LED-GPIO"就是给这次 GPIO request **起一个 label（标签/名称）**，用于标识这个 GPIO 是被谁申请的。

**4、查看gpio占用的指令：**

cat /sys/kernel/debug/gpio