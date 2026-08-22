# Linux 开发板查看 CPU 温度

## 一、查看温度

```bash
cat /sys/class/thermal/thermal_zone0/temp
```

结果通常是毫摄氏度，除以 1000 得到摄氏度：

```bash
echo "scale=2; $(cat /sys/class/thermal/thermal_zone0/temp) / 1000" | bc
```

---

## 二、查看所有温度传感器

```bash
ls /sys/class/thermal/

for zone in /sys/class/thermal/thermal_zone*; do
    echo "$zone: $(cat $zone/temp)"
done
```

---

## 三、说明

| 文件 | 含义 |
|------|------|
| `/sys/class/thermal/thermal_zone0/temp` | 温度值（毫摄氏度） |
| `/sys/class/thermal/thermal_zone0/type` | 传感器类型 |
| `/sys/class/thermal/thermal_zone0/trip_point_*` | 温度触发点 |
