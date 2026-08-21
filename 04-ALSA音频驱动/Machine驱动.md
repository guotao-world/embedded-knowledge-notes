# Machine驱动(硬件板卡的音频系统配置文件)

**定义dai_link**：

```c
static struct snd_soc_dai_link smdk_dai[] = {
{
.name = "WM8994 AIF1", // 链路名称
.stream_name = "Pri_Dai", // 用户空间可见的名称
.cpu_dai_name = "samsung-i2s.0", // CPU DAI
.codec_dai_name = "wm8994-aif1", // Codec DAI，指定了**该芯片上的哪个数字音频接口**
.platform_name = "samsung-audio", // Platform的DMA
.codec_name = "wm8994-codec", // Codec设备名，指定了**哪个音频编解码芯片**
.init = smdk_wm8994_init_paiftx, // 初始化函数
.ops = &smdk_ops, // 操作函数集
},
// ... 可能还会有其他链路 ...
};
```

**定义并注册snd_soc_card**：

```c
static struct snd_soc_card smdk = {
.name = "SMDK-I2S", // 声卡最终名称
.owner = THIS_MODULE,
.dai_link = smdk_dai, // 将上面定义的DAI Link关联
.num_links = ARRAY_SIZE(smdk_dai), // DAI Link的数量
};
```

**在代码中的对应关系**

在 Codec 驱动（例如wm8994.c）中，通常会定义多个snd_soc_dai_driver结构体，其中的.name字段就对应codec_dai_name：

```c
static struct snd_soc_dai_driver wm8994_dai[] = {
{
.name = "wm8994-aif1", // 这就是 codec_dai_name 要匹配的值
...
},
{
.name = "wm8994-aif2",
...
},
};
```

**设备树：**

```dts
sound {compatible ="fsl,imx6ul-evk-wm8960","fsl,imx-audio-wm8960";model ="wm8960-audio";cpu-dai = <&sai2>;audio-codec = <&codec1 &codec2>;asrc-controller = <&asrc>;codec-master;gpr = <&gpr4 0x10000 0x10000>;/** hp-det = <hp-det-pin hp-det-polarity>;* hp-det-pin: JD1 JD2  or JD3* hp-det-polarity = 0: hp detect high for headphone* hp-det-polarity = 1: hp detect high for speaker*/hp-det = <3 0>;/* hp-det-gpios = <&gpio5 4 0>;mic-det-gpios = <&gpio5 4 0>; */audio-routing ="Headphone Jack","HP_L","Headphone Jack","HP_R","Ext Spk","SPK_LP","Ext Spk","SPK_LN","Ext Spk","SPK_RP","Ext Spk","SPK_RN","LINPUT2","Mic Jack","LINPUT3","Mic Jack","RINPUT1","Main MIC","RINPUT2","Main MIC","Mic Jack","MICB","Main MIC","MICB","CPU-Playback","ASRC-Playback","Playback","CPU-Playback","ASRC-Capture","CPU-Capture","CPU-Capture","Capture";};
```

-   **audio-routing的规则：**它由多个"句子"组成，**每个句子是一对字符串（成对出现）**，例如"Headphone Jack", "HP_L"。这里：第一个字符串是**终点 (Sink)**，即信号的接收者。第二个字符串是**起点 (Source)**，即信号的发出者。这个配对表达的就是"将

-   **Source**

-   连接到

-   **Sink**

-   "。