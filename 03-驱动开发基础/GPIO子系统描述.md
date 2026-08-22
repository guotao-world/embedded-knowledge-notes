# GPIO 子系统描述

## 一、设备树固定写法

GPIO 子系统在设备树中的固定格式：

```
< phandle  pin  flags >
```

示例：

```dts
<&gpio0 RK_PC0 GPIO_ACTIVE_HIGH>
```

结构解析：

```
<&gpio0     RK_PC0       GPIO_ACTIVE_HIGH>
    │           │                  │
    │           │                  │
    │           │                  └─ 有效电平（flags）
    │           └──────────────────── GPIO 引脚（pin）
    └──────────────────────────────── GPIO 控制器（phandle）
```

---

## 二、驱动中获取 GPIO 号

### 1. `of_get_named_gpio`

```c
of_get_named_gpio(np, "beep-gpios", 0);
```

第三个参数 `0` 为 **index**——第几个 GPIO。这个属性里可能有多个 GPIO，通过 index 取第几个。

设备树示例：

```dts
led-gpios = <&gpio1 3 GPIO_ACTIVE_HIGH>,
            <&gpio1 4 GPIO_ACTIVE_LOW>;
```

驱动中获取：

```c
of_get_named_gpio(np, "led-gpios", 0);  // gpio1_3
of_get_named_gpio(np, "led-gpios", 1);  // gpio1_4
```

### 2. 解析流程

```c
gpioled.led_gpio = of_get_named_gpio(gpioled.nd, "led-gpio", 0);
```

```
<&gpio0 RK_PC0 GPIO_ACTIVE_HIGH>
          │
          │ 经过 GPIO 控制器解析
          ▼
      Linux GPIO 号
          │
          ▼
    gpioled.led_gpio
```

---

## 三、申请 GPIO

```c
gpio_request(gpioled.led_gpio, "LED-GPIO");
```

第二个参数 `"LED-GPIO"` 是给这次 GPIO request 起一个 **label（标签/名称）**，用于标识这个 GPIO 是被谁申请的。

---

## 四、查看 GPIO 占用情况

```bash
cat /sys/kernel/debug/gpio
```

可以看到每个 GPIO 控制器下各引脚的状态、当前电平、以及申请它的驱动 label。
