# linux开发板查看CPU温度

**查看温度：**

cat /sys/class/thermal/thermal_zone0/temp

**结果通常是毫摄氏度，除以1000得到摄氏度：**

echo "scale=2; $(cat /sys/class/thermal/thermal_zone0/temp) / 1000" | bc

**查看所有温度传感器：**

ls /sys/class/thermal/
for zone in /sys/class/thermal/thermal_zone*; do
    echo "$zone: $(cat $zone/temp)"
done