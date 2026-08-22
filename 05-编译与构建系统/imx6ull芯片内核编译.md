# imx6ull 芯片内核编译

## 一、在内核中增加打印

在内核源码中添加 `printk()` 调试语句，重新编译后烧录。

---

## 二、编译内核中的 sound 声卡

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/generic/
make -C ../../../ -j16
```

### 编译好的内核位置

```bash
cd ../../../arch/arm/boot/
```

---

## 三、编译内核中的 codec 驱动

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/codecs/
make -C ../../../ -j16
cd ../../../arch/arm/boot/
```

---

## 四、拷贝内核到 eMMC

```bash
scp ../../../arch/arm/boot/zImage root@192.168.55.71:/run/media/mmcblk1p1/
```

---

## 五、搜索文件中的字符串

```bash
grep -rn "你要找的字符" ./
grep -rn "bitclock-master" ../../
```
