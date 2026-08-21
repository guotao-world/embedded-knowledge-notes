# Kconfig 讲解

## Q：Kconfig 是什么？

**A：** Kconfig 负责产生 `.config`，Kbuild 负责把 `.config` 导入 Make 环境，Makefile 通过 `$(CONFIG_xxx)` 使用这些配置。

这也是为什么 Linux 驱动添加流程永远是：

```
Kconfig → .config → Makefile → 编译产物
```

---

## Kconfig 语法

### 1. config —— 定义一个配置项

最基本：

```kconfig
config SND_SOC_MY_DUMMY_CODEC
```

意思：定义一个配置项 `CONFIG_SND_SOC_MY_DUMMY_CODEC`，最终会出现在 `.config` 中。

---

### 2. tristate —— 三态配置（驱动最常用）

例如：

```kconfig
config SND_SOC_MY_DUMMY_CODEC
    tristate "My dummy codec"
```

对应 menuconfig 中的三种状态：

- `<M> My dummy codec` —— 编译为模块
- `[*] My dummy codec` —— 编译进内核
- `< > My dummy codec` —— 不编译

---

### 5. 数字类型

```kconfig
integer
config BUFFER_SIZE
    int "buffer size"
    default 1024
```

生成：

```
CONFIG_BUFFER_SIZE=1024
```

---

### 6. depends on —— 依赖

非常重要。

例如：

```kconfig
config SND_SOC_MY_CODEC
    tristate "My codec"
    depends on SND_SOC
```

意思：必须开启 `CONFIG_SND_SOC` 才能看到 `My codec`。

多个依赖：

```kconfig
depends on I2C && SND_SOC   # 两个都需要
depends on I2C || SPI       # 二选一
```

---

### 7. select —— 自动选择

例如：

```kconfig
config SND_SOC_AC97_CODEC
    tristate
    select SND_AC97_CODEC
```

意思：如果打开 `SND_SOC_AC97_CODEC`，自动打开 `SND_AC97_CODEC`。

关系：选择 A → 自动打开 B。

> 注意：`select` 要谨慎，因为它不会检查依赖。官方更推荐 `depends on`，而不是大量使用 `select`。

---

### 8. default —— 默认值

默认开启：

```kconfig
config TEST
    bool
    default y
```

条件默认：

```kconfig
config SND_SOC_I2C_AND_SPI
    tristate
    default m if I2C=m
    default y if I2C=y
```

意思：
- 如果 `I2C=m`，那么 `SND_SOC_I2C_AND_SPI=m`
- 如果 `I2C=y`，那么 `SND_SOC_I2C_AND_SPI=y`

---

### 9. help —— 帮助说明

例如：

```kconfig
config SND_SOC_MY_DUMMY_CODEC
    tristate "My dummy codec"
    depends on SND_SOC
    help
      Minimal dummy codec driver.
      This driver is used for testing.
```

在 `make menuconfig` 里面按 `?` 会显示帮助内容。

> 注意：必须另起一行，而且 help 后面的帮助内容必须比 help 多一级缩进。
>
> Kconfig 语法中，`help` 本身只是一个关键字，它告诉解析器：接下来缩进更深的多行文本都是帮助信息。

---

### 10. menu —— 创建菜单

例如：

```kconfig
menu "CODEC drivers"

config SND_SOC_WM8960
    tristate "WM8960 codec"

endmenu
```

效果：

```
Sound
|
+-- CODEC drivers
    |
    +-- WM8960 codec
```

---

### 11. menuconfig

特殊形式：

```kconfig
menuconfig SOUND
    bool "Sound card support"
```

它既是一个配置项，也是一个菜单入口。

例如内核中的：

```
Device Drivers
|
+-- Sound card support
```

就是 `menuconfig SOUND`。

---

### 12. if / endif

条件区域：

```kconfig
if SND_SOC

config SND_SOC_MY_CODEC
    tristate "My codec"

endif
```

等价于每个 config 都写 `depends on SND_SOC`。

---

### 13. source

包含其他 Kconfig：

例如顶层：

```kconfig
source "sound/Kconfig"
```

进入 `sound/Kconfig`，然后：

```kconfig
source "sound/soc/Kconfig"
```

继续展开，最终形成整个配置菜单。

---

### 14. ASoC Codec 驱动典型 Kconfig

你的 dummy codec：

```kconfig
config SND_SOC_MY_DUMMY_CODEC
    tristate "My dummy codec"
    depends on SND_SOC
    help
      Minimal dummy codec driver
```

这是最标准写法。

对应 Makefile：

```makefile
obj-$(CONFIG_SND_SOC_MY_DUMMY_CODEC) += my_dummy_codec.o
```

---

## 编译流程图

```
make zImage
    |
    v
根目录 Makefile
    |
    v
读取 .config
    |
    v
生成/加载 auto.conf
    |
    v
进入 arch/arm
    |
    v
进入 drivers
    |
    v
进入 sound
    |
    v
进入 sound/soc/codecs
    |
    v
读取 Makefile
    |
    v
obj-$(CONFIG_xxx)
    |
    v
展开为 obj-m += xxx.o
    |
    v
gcc 编译
```
