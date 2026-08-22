# Linux 音频驱动编译调试流程（ALSA 编译调试）

## 一、查看声卡

```bash
cat /proc/asound/cards
aplay -l
```

## 二、查看硬件参数

```bash
aplay --dump-hw-params -D hw:0,0
arecord --dump-hw-params -D hw:0,0
```

## 三、在源代码中搜索关键字

```bash
grep -rn "dai-tdm-slot" sound/soc/
```

## 四、播放测试

### 播放 WAV 文件

```bash
aplay MIX1.wav
aplay -D hw:0,0 MIX1.wav
```

### 播放裸 PCM

```bash
aplay -D hw:0,0 -r 8000 -f S16_LE -c 2 -t raw test.pcm
```

## 五、录音测试

```bash
arecord -D hw:0,0 -r 8000 -f S16_LE -c 2 -d 5 test.wav
```

### 各参数说明

| 参数 | 含义 | 示例 |
|------|------|------|
| `-D hw:0,0` | card0 device0 | `hw:0,0` |
| `-r 8000` | 8kHz 采样率 | `8000` |
| `-f S16_LE` | 16bit little endian | `S16_LE` |
| `-c 2` | 双声道 | `2` |
| `-t raw` | 裸 PCM 数据 | `raw` |

## 六、查看设备树

```bash
ls /proc/device-tree
cat /proc/device-tree/model
```

## 七、查看声卡

```bash
cat /proc/asound/cards
```

## 八、查看设备树的更新时间

```bash
ls -l /run/media/mmcblk0p1/
```

## 九、ALSA 简单声卡支持（编译内核选项）

```bash
make menuconfig
# Device Drivers
#   -> Sound card support
#      -> Advanced Linux Sound Architecture
#         -> ALSA for SoC audio support
#            -> ASoC Simple sound card support
```

## 十、验证声卡（simple-card）

```bash
uname -a
cat /proc/asound/cards
cat /proc/device-tree/sound/compatible
cat /proc/device-tree/sound/simple-audio-card,name
ls /proc/device-tree/sound/
dmesg | grep -i sound
dmesg | grep -i asoc
dmesg | grep "my-codec"
dmesg | grep "asoc"
dmesg | grep " asoc-simple-card"
```

## 十一、MD5 校验

### Ubuntu 端

```bash
md5sum ../../../arch/arm/boot/zImage
ssh root@192.168.55.71 md5sum /run/media/mmcblk1p1/zImage
```

### 开发板端

```bash
md5sum /run/media/mmcblk1p1/zImage
```

## 十二、在编译了的内核中查找某个字符串

```bash
strings ../../../arch/arm/boot/zImage | grep "probe"
grep -a "my dummy codec probe" ../../../arch/arm/boot/zImage
```

## 十三、编译内核中的 sound 声卡

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/generic/
make -C ../../../ -j16
cd ../../../arch/arm/boot/
```

## 十四、编译 codec 驱动

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/codecs/
make -C ../../../ -j16
cd ../../../arch/arm/boot/
```

## 十五、拷贝内核到 eMMC

```bash
scp ../../../arch/arm/boot/zImage root@192.168.55.71:/run/media/mmcblk1p1/
```
