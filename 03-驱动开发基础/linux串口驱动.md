# linux串口驱动

**总体流程图：**

DTS

│

│

compatible=fsl,imx6q-uart

│

↓

platform_driver匹配

│

↓

serial_imx_probe()

│

----------------------------------------

│ │ │ │

获取reg 获取irq 获取clock 配置uart_port

│ │ │ │

ioremap request_irq clk_get uart_ops

│

│

↓

uart_add_one_port()

│

│

↓

serial core

│

│

↓

/dev/ttymxc0