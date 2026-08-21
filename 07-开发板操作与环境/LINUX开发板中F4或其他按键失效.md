# LINUX开发板中F4或其他按键失效

使用此指令

export TERM=xterm-256color

或永久

echo 'export TERM=xterm-256color' >> ~/.bashrc
source ~/.bashrc

**source命令：**

source script.sh = "在当前 shell 里复制粘贴执行脚本内容"
./script.sh = "开一个新 shell 去执行"