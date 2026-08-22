# 编译设备树

## 一、查看当前 Linux 内核使用的设备树

> 默认是 `imx6ull-14x14-emmc-4.3-480x272-c.dts`，改成别的也被刷掉，暂未解决。

```bash
# 查看根节点的 compatible 属性，这会显示板子的兼容性字符串
cat /proc/device-tree/compatible | tr '\0' '\n'

# 查看根节点的 model 属性
cat /proc/device-tree/model | tr '\0' '\n'
```

---

## 二、使用 U-Boot 打印当前设备树

```bash
=> print fdt_file
fdt_file=imx6ull-14x14-emmc-4.3-480x272-c.dtb
```

或

```bash
=> printenv
```

---

## 三、使用 U-Boot 修改设备树

```bash
=> setenv fdt_file imx6ull-14x14-emmc-4.3-800x480-c.dtb
=> saveenv    # 保存到环境变量存储区（如 MMC、Flash）
=> boot
```

### 救砖

```bash
setenv fdt_file imx6ull-14x14-evk-emmc.dtb
```

---

## 四、编译设备树

### 设置交叉编译器

```bash
export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
```

### 设备树文件在内核源码

```bash
cd arch/arm/boot/dts
```

### 在 dts 目录下编译

```bash
make -C ../../../../ dtbs
```

### 在内核路径下编译

```bash
make dtbs
```

> 注意：若遇到权限问题，则可以 `chmod -R u+w /home/zhangxin/workspace_imx6ull/kernel`

---

## 五、拷贝

```bash
cp imx6ull-14x14-emmc-4.3-480x272-c.dtb temp/
cp -v imx6ull-14x14-emmc-4.3-480x272-c.dtb /home/zhangxin/linuxShare/
```

### 拷贝 SCP 到 eMMC

```bash
scp imx6ull-14x14-emmc-4.3-480x272-c.dtb root@192.168.55.71:/run/media/mmcblk1p1/
```

---

## 六、切换到 boot 文件夹

```bash
cd /run/media/mmcblk1p1
```

---

## 七、打印内核信息

```bash
dmesg | grep "failed to enable bus clock"
```

---

## 八、列出当前的设备节点

```bash
ls /proc/device-tree
```

### 查看设备节点

```bash
for f in *; do
    echo "---- $f ----"
    hexdump -C "$f"
done
```

---

## 九、救砖（开发板输入）

```bash
cp /run/media/mmcblk0p1/imx6ull-14x14-emmc-4.3-480x272-c_bak.dtb \
   /run/media/mmcblk0p1/imx6ull-14x14-emmc-4.3-480x272-c.dtb
```

---

## 十、反编译

进入 `kernel/scripts/dtc` 路径：

```bash
./dtc -I dtb -O dts imx6ull-14x14-emmc-4.3-480x272-c.dtb -o imx6ull-14x14-emmc-4.3-480x272-c.dts
```

---

## 十一、找 phandle 的最大值

```bash
grep phandle imx6ull-14x14-emmc-4.3-480x272-c.dts
```

当前最大值 `0x4e`，因此保险起见使用：

```dts
phandle = <0x50>;
```
