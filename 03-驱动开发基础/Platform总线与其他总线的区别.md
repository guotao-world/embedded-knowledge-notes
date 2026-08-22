# Platform 总线与其他总线的区别

## 一、Platform Bus 的设计目的（官方描述）

内核文档中明确说明：

> "This pseudo-bus is used to connect devices on buses with **minimal infrastructure**, like those used to integrate peripherals on many **system-on-chip (SoC)** processors, or some legacy PC interconnects; as opposed to large formally specified ones like PCI or USB."

简单说：Platform Bus 是给"**没有正规总线基础设施**"的设备准备的虚拟总线。

---

## 二、枚举逻辑 vs 非枚举逻辑

**枚举逻辑（Enumeration Logic）**和**非枚举逻辑（Non-Enumeration / Non-Discoverable Logic）**是 Linux 内核设备模型中非常重要的两个概念，它们描述了设备被"发现"的方式完全不同。

### 1. 什么是"枚举逻辑"？

**枚举** = 内核（或硬件）主动去"扫描、发现、识别"设备的过程。

典型代表：PCI、USB —— 硬件可以自动探测总线上挂了什么设备。

### 2. 什么是"非枚举逻辑"？

**非枚举** = 设备**无法被硬件自动发现**，必须由**软件提前静态告知**内核设备存在。

典型代表：Platform 总线、I2C、SPI —— 设备必须通过设备树（DTS）或板级代码静态描述。

---

## 三、对比总结

| 总线类型 | 发现方式 | 典型代表 |
|---------|---------|---------|
| 可枚举总线 | 硬件自动扫描 | PCI、USB |
| 非枚举总线 | 软件静态描述（DTS/ACPI） | Platform、I2C、SPI |

Platform 总线之所以存在，就是因为 SoC 内部的很多外设（如 UART、GPIO、定时器等）没有像 PCI 那样的自描述能力，需要一个虚拟总线来统一管理。
