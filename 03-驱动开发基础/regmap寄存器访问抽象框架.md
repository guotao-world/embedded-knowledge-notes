# regmap 寄存器访问抽象框架

## 一、regmap 的两种工作模式（非常重要）

### ① 标准寄存器模式

```
regmap_read(reg)
    ↓
自动加 read_flag_mask
    ↓
SPI burst
```

**适用：** IMU / codec / sensor 等有标准寄存器地址的芯片。

### ② 自定义 IO 模式

```
regmap_read(reg)
    ↓
调 reg_read callback
    ↓
你自己拼 SPI 命令
```

**适用：** Flash / NAND / FPGA 等没有标准寄存器地址映射的设备。

---

## 二、对比总结

| 模式 | 数据传输方式 | 典型设备 |
|------|------------|---------|
| 标准寄存器模式 | regmap 自动拼地址+数据，burst 传输 | IMU、codec、sensor |
| 自定义 IO 模式 | 驱动自己实现 read/write callback | Flash、NAND、FPGA |
