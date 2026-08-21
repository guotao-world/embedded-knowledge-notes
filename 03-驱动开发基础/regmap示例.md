# regmap示例

**举一个真实工程例子（UART音频芯片）**

**你一般会定义：**

```c
struct uart_audio_dev {
int uart_fd;
struct mutex lock;
uint8_t tx_buf[256];
};
struct uart_audio_dev *dev = kzalloc(...);
dev->uart_fd = open_uart();
```

**初始化 regmap：**

```c
map = regmap_init(&uart_bus,
dev,
&cfg);
```

**在 bus 里怎么用？**

```c
static int uart_write(void *context,
const void *data,
size_t count)
{
struct uart_audio_dev *dev = context;
// 这里就可以访问 UART
write(dev->uart_fd, data, count);
}
```

**read 也是一样：**

```c
static int uart_read(void *context, ...)
{
struct uart_audio_dev *dev = context;
uart_recv(dev->uart_fd, ...);
}
```