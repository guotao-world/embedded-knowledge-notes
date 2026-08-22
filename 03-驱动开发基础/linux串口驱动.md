# Linux 串口驱动

## 一、总体流程图

```
DTS
  │
  │ compatible = "fsl,imx6q-uart"
  ↓
platform_driver 匹配
  ↓
serial_imx_probe()
  │
  ├──────┬──────┬──────┬──────────┐
  │      │      │      │          │
获取reg 获取irq 获取clock 配置uart_port
  │      │      │      │
ioremap request_irq clk_get  uart_ops
  │
  ↓
uart_add_one_port()
  │
  ↓
serial core
  │
  ↓
/dev/ttymxc0
```

---

## 二、关键步骤说明

| 步骤 | 函数/操作 | 作用 |
|------|----------|------|
| 获取 reg | `platform_get_resource()` | 获取寄存器物理地址 |
| 地址映射 | `devm_ioremap()` | 物理地址 → 虚拟地址 |
| 获取 irq | `platform_get_irq()` | 获取中断号 |
| 注册中断 | `devm_request_irq()` | 注册收发中断处理函数 |
| 获取 clock | `devm_clk_get()` | 获取串口时钟 |
| 使能时钟 | `clk_prepare_enable()` | 开启外设时钟 |
| 配置 port | `uart_ops` + `uart_port` | 填充 serial core 需要的操作集 |
| 注册端口 | `uart_add_one_port()` | 向 serial core 注册端口，生成 `/dev/ttymxc0` |
