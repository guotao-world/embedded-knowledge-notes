# regmap 示例

## 一、真实工程例子（UART 音频芯片）

### 定义设备结构体

```c
struct uart_audio_dev {
    int uart_fd;
    struct mutex lock;
    uint8_t tx_buf[256];
};

struct uart_audio_dev *dev = kzalloc(...);
dev->uart_fd = open_uart();
```

### 初始化 regmap

```c
map = regmap_init(&uart_bus, dev, &cfg);
```

### 在 bus 里怎么用？

```c
static int uart_write(void *context, const void *data, size_t count)
{
    struct uart_audio_dev *dev = context;
    // 这里就可以访问 UART
    write(dev->uart_fd, data, count);
}
```

### read 也是一样

```c
static int uart_read(void *context, ...)
{
    struct uart_audio_dev *dev = context;
    uart_recv(dev->uart_fd, ...);
}
```

---

## 二、关键点

- `regmap_init()` 的第二个参数 `dev` 会作为 `context` 传给 `read`/`write` callback
- 通过 `context` 指针，callback 里可以访问到设备的私有数据（如 UART 文件描述符、锁、缓冲区等）
- 这样 regmap 就不局限于 I2C/SPI，任何总线（包括 UART）都可以通过自定义 callback 来适配
