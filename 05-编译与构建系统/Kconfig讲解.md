# Kconfig讲解

**Q：Kconfig是什么**

**A:Kconfig负责产生 .config，Kbuild负责把 .config 导入 Make 环境，Makefile通过 $CONFIG_xxx) 使用这些配置。**这也是为什么 Linux 驱动添加流程永远是：**Kconfig → .config → Makefile → 编译产物**

**Kconfig语法：**

**1. config ------ 定义一个配置项**

最基本：

config SND_SOC_MY_DUMMY_CODEC

意思：

定义一个配置项：

CONFIG_SND_SOC_MY_DUMMY_CODEC

最终会出现在：

.config

**2. tristate ------ 三态配置（驱动最常用）**

例如：

config SND_SOC_MY_DUMMY_CODEC
tristate "My dummy codec"

对应：

<M> My dummy codec

[*] My dummy codec

< > My dummy codec

**5. 数字类型**

**integer**

config BUFFER_SIZE int "buffer size" default 1024

生成：

CONFIG_BUFFER_SIZE=1024

**6. depends on ------ 依赖**

非常重要。

例如：

config SND_SOC_MY_CODEC
tristate "My codec"
depends on SND_SOC

意思： 必须开启：CONFIG_SND_SOC 才能看到：My codec

多个依赖：depends on I2C && SND_SOC 表示：两个都需要。

也可以：depends on I2C || SPI 表示：二选一。

**7. select ------ 自动选择**

例如：config SND_SOC_AC97_CODEC tristate select SND_AC97_CODEC 意思：

如果打开：SND_SOC_AC97_CODEC 自动打开：SND_AC97_CODEC

关系：选择A | v自动打开B

注意：select 要谨慎。 因为它不会检查依赖。 官方更推荐：depends on 而不是大量：select

**8. default ------ 默认值**

例如：默认开启。

config TEST
bool
default y

条件默认：

config SND_SOC_I2C_AND_SPI
tristate
default m if I2C=m
default y if I2C=y

意思：如果：I2C=m 那么：
SND_SOC_I2C_AND_SPI=m 如果：I2C=y 那么：SND_SOC_I2C_AND_SPI=y

**9. help ------ 帮助说明**

例如：

config SND_SOC_MY_DUMMY_CODEC
tristate "My dummy codec"
depends on SND_SOC
help Minimal dummy codec driver. This driver is used for testing.在：makemenuconfig 里面按： ? 会显示。注意：**必须另起一行**，而且 help 后面的帮助内容必须比 help**多一级缩进**。Kconfig 语法中，help 本身只是一个关键字，它告诉解析器：**接下来缩进更深的多行文本都是帮助信息。10. menu ------ 创建菜单**例如：menu "CODEC drivers"config SND_SOC_WM8960 tristate "WM8960 codec"endmenu效果：Sound | +-- CODEC drivers | +-- WM8960 codec**11. menuconfig**特殊形式：menuconfig SOUND bool "Sound card support"它既是：一个配置项一个菜单入口例如：内核：Device Drivers | + Sound card support就是：menuconfig SOUND**12. if / endif**条件区域：if SND_SOCconfig SND_SOC_MY_CODEC tristate "My codec"endif等价：depends on SND_SOC**13. source**包含其他 Kconfig：例如：顶层：source "sound/Kconfig" 进入：sound/Kconfig 然后：source "sound/soc/Kconfig" 继续展开。最终形成整个配置菜单。**14. ASoC Codec 驱动典型 Kconfig**你的 dummy codec：config SND_SOC_MY_DUMMY_CODEC tristate "My dummy codec" depends on SND_SOC help Minimal dummy codec driver这是最标准写法。对应 Makefile：obj-$(CONFIG_SND_SOC_MY_DUMMY_CODEC) += my_dummy_codec.o

**流程图：**make zImage | | v根目录 Makefile | |读取 .config | |生成/加载 auto.conf | |进入 arch/arm | |进入 drivers | |进入 sound | |进入 sound/soc/codecs | |读取 Makefile
obj-$(CONFIG_xxx) | |展开obj-m += xxx.o | |gcc