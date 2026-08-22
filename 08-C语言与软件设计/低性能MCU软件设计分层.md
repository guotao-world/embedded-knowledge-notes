# 低性能 MCU 软件设计分层

## 一、分层设计

如果想在简单的 MCU 上设计芯片结构，可以分这几层：**HAL 层 / Driver 层 / Board 层 / OS 层 / APP 层**。

完全可以，而且这是一个非常清晰、合理的分层设计，符合大多数嵌入式软件工程的最佳实践，尤其是当 MCU 上运行的是 RTOS 或复杂裸机系统时。

```
┌─────────────────────────────────────────┐
│              APP 层                     │  ← 用户应用
├─────────────────────────────────────────┤
│              OS 层                      │  ← RTOS / 调度器
├─────────────────────────────────────────┤
│             BOARD 层                    │  ← 板级功能
├─────────────────────────────────────────┤
│            DRIVER 层                    │  ← 设备驱动
├─────────────────────────────────────────┤
│              HAL 层                     │  ← 硬件抽象
└─────────────────────────────────────────┘
```

---

## 二、关键设计原则（避免混乱）

### 应该做的

- **APP 只调用 OS 和 BOARD 的高层接口**
- **DRIVER 提供设备抽象，而非直接暴露 HAL**
- **BOARD 负责"组装"，将 DRIVER 实例和具体硬件绑定**

---

## 三、可能的改进建议

根据项目复杂度：

1. **小型项目（<1 万行）**：合并 HAL+DRIVER 或 DRIVER+BOARD
2. **中型项目**：当前的 5 层完全合适
3. **大型项目**：可在 APP 和 OS 之间加 **SERVICE 层**（协议、文件系统、日志等）

### 是否需要 SERVICE 层？

如果应用复杂（例如需要网络协议栈、加密、日志系统），建议：

```
APP → SERVICE → OS → BOARD → DRIVER → HAL
```

SERVICE 层提供可复用的中间件组件。

---

## 四、总结

分层设计非常优秀，是嵌入式软件工程的标准范式。关键是**严格遵守依赖方向**，并确保：

- **BOARD 层是唯一知道"硬件如何连接"的地方**
- **DRIVER 层只关心"某类设备的通用逻辑"**
- **HAL 层只关心"芯片寄存器"**

这样设计出来的代码，换芯片时只需重写 HAL+DRIVER（或部分），换板子只需修改 BOARD 层，换应用场景只需修改 APP 层，维护成本极低。

---

## 五、实际代码示例

```c
// ========== hal_gpio.c ==========
void hal_gpio_set(uint32_t pin) {
    GPIO_BASE[pin/32] |= (1 << (pin%32));
}

// ========== driver_led.c ==========
static struct led_dev {
    uint32_t pin;
} leds[LED_MAX];

void led_init(int id, uint32_t pin) {
    leds[id].pin = pin;
    hal_gpio_set_mode(pin, OUTPUT);
}

void led_on(int id) {
    hal_gpio_set(leds[id].pin);
}

// ========== board.c ==========
void board_init(void) {
    led_init(0, BOARD_LED1_PIN);
    led_init(1, BOARD_LED2_PIN);
}

// ========== app.c (使用 RTOS) ==========
void app_task(void *arg) {
    while(1) {
        led_on(0);
        os_delay(1000);  // OS 层延时
        led_off(0);
        os_delay(1000);
    }
}
```
