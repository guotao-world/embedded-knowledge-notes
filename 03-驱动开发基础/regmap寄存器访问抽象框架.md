# regmap寄存器访问抽象框架

**regmap的两种工作模式（非常重要）**

**① 标准寄存器模式（你现在ICM20608）**

regmap_read(reg)→ 自动加 read_flag_mask→ SPI burst

✔ 适用：IMU / codec / sensor

**② 自定义IO模式（Flash / NAND）**

regmap_read(reg)→ 调 reg_read callback→ 你自己拼 SPI命令

✔ 适用：Flash / NAND / FPGA