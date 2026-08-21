# ALSA的设备树示例

```dts
my_codec: my-codec {
compatible ="my,dummy-codec";
#sound-dai-cells = <0>;
};
sound {
compatible ="simple-audio-card";
simple-audio-card,name ="imx6ull-dummy-test";
simple-audio-card,format ="i2s";
/*
* CPU作为master
*/
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
&sai2 {
pinctrl-names ="default";
pinctrl-0 = <&pinctrl_sai2>;
#sound-dai-cells = <0>;
assigned-clocks = <&clks IMX6UL_CLK_SAI2_SEL>,
<&clks IMX6UL_CLK_SAI2>;
assigned-clock-parents = <&clks IMX6UL_CLK_PLL4_AUDIO_DIV>;
// assigned-clock-rates = <0>, <11289600>;
assigned-clock-rates = <0>, <12288000>;
// assigned-clock-rates = <0>, <4096000>;
status ="okay";
};
```