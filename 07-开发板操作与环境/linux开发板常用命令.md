# linux开发板常用命令

**文件操作：**

ls -la # 列出所有文件（含隐藏）
cp -r 源 目标 # 递归复制
mv 源 目标 # 移动/重命名
rm -rf 目录 # 强制删除
mkdir -p a/b/c # 创建多级目录
touch filename # 创建空文件

**查看文件：**

cat filename # 查看全部
less filename # 分页查看
tail -f filename # 实时跟踪末尾
head -n 20 filename # 查看前20行

**查找：**

find / -name "*.c" # 按名称查找
grep -rn "关键词" ./ # 递归搜索内容
which command # 查找命令位置

**网络：**

ifconfig # 查看网络接口
ping IP # 测试连通性
netstat -tlnp # 查看监听端口
ssh user@IP # 远程登录

**进程：**

ps aux # 查看所有进程
kill PID # 终止进程
kill -9 PID # 强制终止
top # 实时监控

**系统：**

reboot # 重启
shutdown -h now # 立即关机
dmesg | tail # 查看内核日志
lsmod # 查看已加载模块
insmod module.ko # 加载模块
rmmod module # 卸载模块