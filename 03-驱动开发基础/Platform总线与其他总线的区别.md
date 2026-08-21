# Platform总线与其他总线的区别

**Platform Bus 的设计目的（官方描述）**

内核文档中明确说明：

"This pseudo-bus is used to connect devices on buses with**minimal infrastructure**, like those used to integrate peripherals on many**system-on-chip (SoC)**processors, or some legacy PC interconnects; as opposed to large formally specified ones like PCI or USB."

简单说：Platform Bus 是给"**没有正规总线基础设施**"的设备准备的虚拟总线。

**枚举逻辑（Enumeration Logic）**和**非枚举逻辑（Non-Enumeration / Non-Discoverable Logic）**是 Linux 内核设备模型中非常重要的两个概念，它们描述了**设备被"发现"的方式**完全不同。

**1. 什么是"枚举逻辑"（Enumeration Logic）？**

**枚举**= 内核（或硬件）主动去"扫描、发现、识别"设备的过程。

**2. 什么是"非枚举逻辑"（Non-Discoverable Logic）？**

**非枚举**

= 设备

**无法被硬件自动发现**

，必须由

**软件提前静态告知**

内核设备存在。