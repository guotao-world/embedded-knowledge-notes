# ALSA 的设备树示例

## 一、simple-audio-card 示例

```dts
my_codec: my-codec {
    compatible = "my,dummy-codec";
    #sound-dai-cells = <0>;
};

sound {
    compatible = "simple-audio-card";
    simple-audio-card,name = "imx6ull-dummy-test";
    simple-audio-card,format = "i2s";

    /* CPU 作为 master */
    simple-audio-card,bitclock-master = <&cpu_dai>;
    simple-audio-card,frame-master = <&cpu_dai>;

    cpu_dai: simple-audio-card,cpu {
        sound-dai = <&sai2>;
        dai-tdm-slot-num = <2>;
        dai-tdm-slot-width = <16>;
        system-clock-frequency = <12288000>;
    };

    codec_dai: simple-audio-card,codec {
        sound-dai = <&my_codec>;
        dai-tdm-slot-num = <2>;
        dai-tdm-slot-width = <16>;
    };
};
```

---

## 二、SAI 控制器配置

```dts
&sai2 {
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_sai2>;
    #sound-dai-cells = <0>;

    assigned-clocks = <&clks IMX6UL_CLK_SAI2_SEL>,
                      <&clks IMX6UL_CLK_SAI2>;
    assigned-clock-parents = <&clks IMX6UL_CLK_PLL4_AUDIO_DIV>;
    /* assigned-clock-rates = <0>, <11289600>; */
    assigned-clock-rates = <0>, <12288000>;
    /* assigned-clock-rates = <0>, <4096000>; */

    status = "okay";
};
```

---

## 三、关键字段说明

| 字段 | 作用 |
|------|------|
| `simple-audio-card,name` | 声卡名称，用户空间可见 |
| `simple-audio-card,format` | 音频格式（i2s / dsp_a / left_j 等） |
| `simple-audio-card,bitclock-master` | 指定位时钟主设备 |
| `simple-audio-card,frame-master` | 指定帧时钟主设备 |
| `sound-dai` | 引用 CPU DAI 或 Codec DAI |
| `dai-tdm-slot-num` | TDM 时隙数量 |
| `dai-tdm-slot-width` | TDM 时隙宽度（bit） |
| `system-clock-frequency` | 系统时钟频率（Hz） |
