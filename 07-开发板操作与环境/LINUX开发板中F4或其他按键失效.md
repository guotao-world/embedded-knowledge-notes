# LINUX 开发板中 F4 或其他按键失效

## 一、解决方法

使用此指令：

```bash
export TERM=xterm-256color
```

或永久设置：

```bash
echo 'export TERM=xterm-256color' >> ~/.bashrc
source ~/.bashrc
```

---

## 二、source 命令

| 命令 | 区别 |
|------|------|
| `source script.sh` | 在当前 shell 里复制粘贴执行脚本内容 |
| `./script.sh` | 开一个新 shell 去执行 |

> `source` 执行的脚本中修改的环境变量会影响当前 shell，而 `./` 方式不会。
