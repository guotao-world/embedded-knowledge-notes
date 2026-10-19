# Python subprocess 模块讲解

> 在 Python 程序里"调用外部命令"：启动另一个程序、执行 shell 命令、把结果收回来。
> 适合自动化脚本场景：跑系统命令、ping 测试、启动工具等。

---

## 1. subprocess 是什么

subprocess 是 Python 标准库模块，作用是在你的 Python 程序里**运行外部命令**——相当于在命令行里敲了一句命令，但还能拿到它的输出和退出码。

应用场景：

- ping 网络测试；
- 调用系统命令（ls / dir / 查看文件）；
- 启动外部程序（记事本、工具链）；
- 自动化脚本里判断"命令是否成功"。

---

## 2. 三种调用方式对比

| 方式 | 等不等它结束 | 能不能拿输出 | 适用场景 |
|---|---|---|---|
| os.system() | 等 | 拿不到 | 旧代码、最简单，认识即可 |
| subprocess.run() | 等 | 能（stdout / stderr / returncode） | **最常用，推荐** |
| subprocess.Popen() | 不等 | 能（异步读） | 启动后继续干别的 |

### 2.1 os.system() —— 最简单（旧方法，认识即可）

```python
import os
os.system("notepad.exe")     # 等于在命令行敲了一句，但拿不到输出
```

局限：返回值只有一个退出码，拿不到程序打印的内容。它是 subprocess 出现之前的旧方法，新代码推荐用 subprocess。

### 2.2 subprocess.run() —— 最常用（推荐）

```python
import subprocess

r = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],   # 注意用列表传参，不用拼字符串
    capture_output=True,                # 捕获输出
    text=True                           # 把输出转成文本
)

print(r.returncode)   # 退出码：0 表示成功，非 0 是失败
print(r.stdout)       # 程序打印的标准输出
print(r.stderr)       # 错误输出
```

**拓展一：失败即报错（check=True）**

默认退出码非 0 只是放在 r.returncode 里，程序不会停。想要"命令失败就直接抛异常"：

```python
r = subprocess.run(["ping", "-n", "2", "127.0.0.1"],
                   capture_output=True, text=True, check=True)
# 退出码非 0 → 抛 subprocess.CalledProcessError，程序立刻报错
```

**拓展二：超时保护（timeout）**

命令卡住不返回时，timeout 秒后抛 TimeoutExpired，防止程序挂死：

```python
r = subprocess.run(["ping", "-n", "10", "127.0.0.1"],
                   capture_output=True, text=True, timeout=3)
# 3 秒没跑完 → 抛 subprocess.TimeoutExpired
```

### 2.3 subprocess.Popen() —— 底层，不等待

run() 会一直等到命令跑完；Popen 是"发令枪响就走"，启动后你的程序继续干别的：

```python
import subprocess

p = subprocess.Popen(["notepad.exe"])
# ... 启动后继续做别的事 ...
p.wait()              # 需要时再等它结束

# 想拿输出：communicate() 等它结束并收回报文
p = subprocess.Popen(["ping", "-n", "2", "127.0.0.1"],
                     stdout=subprocess.PIPE, text=True)
out, err = p.communicate()     # 阻塞直到结束，返回 (stdout, stderr)
print(out)
```

run() 其实就是"Popen + communicate + 等结束"的封装——平时用 run() 就够了，Popen 只有需要"边跑边干活"时才用。

---

## 3. 常用参数一览

| 参数 | 作用 |
|---|---|
| capture_output=True | 捕获 stdout 和 stderr（默认不捕获，直接打到终端） |
| text=True | 输出转成文本字符串（否则是 bytes 字节流，要 .decode()） |
| check=True | 退出码非 0 时抛 CalledProcessError |
| timeout=秒 | 超过时间抛 TimeoutExpired |
| cwd="路径" | 在指定目录下运行命令 |
| shell=True | 是否经 shell 解析（**默认 False，安全**，见第 4 节） |

---

## 4. 安全提醒：列表传参，慎用 shell=True

**安全写法（默认推荐）：** 列表传参，命令和参数分开，参数就是参数：

```python
subprocess.run(["ping", "-n", "2", "127.0.0.1"])
```

**危险写法（别学）：** 字符串拼接 + shell=True，如果参数里有用户输入，可能被当成命令执行（命令注入，类似 C 语言的 system() 漏洞）：

```python
# ❌ 别这么写：user_input 里若含特殊字符，可能被 shell 解析成新命令
subprocess.run("ping -n 2 " + user_input, shell=True)
```

心法：**能用列表传参就不要碰 shell=True**；真的需要 shell 特性时，也绝不把不可信的输入拼进命令字符串。

---

## 5. 嵌入式 / 日常场景示例

```python
import subprocess

# 例 1：ping 测试判断设备是否在线
# 注意：Windows 用 -n，Linux/开发板用 -c
r = subprocess.run(["ping", "-n", "2", "192.168.1.1"],
                   capture_output=True, text=True)
if r.returncode == 0:
    print("device reachable")
else:
    print("device unreachable")

# 例 2：跑命令看结果（开发板上查看文件等）
r = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print(r.stdout)

# 例 3：命令失败要"立刻知道"
try:
    subprocess.run(["some_tool"], check=True)
except subprocess.CalledProcessError as e:
    print(f"tool failed, exit code: {e.returncode}")
```

---

## 6. 初学阶段需要掌握的内容

记住最常用的一条就够了：

```python
import subprocess

r = subprocess.run(["命令", "参数1", "参数2"], capture_output=True, text=True)

if r.returncode == 0:      # 成功
    print(r.stdout)        # 看输出
else:                      # 失败
    print(r.stderr)        # 看错误
```

---

## 总结

- **subprocess.run() 是主力**：列表传参 + capture_output + text，能拿退出码、标准输出、错误输出；
- **os.system() 认识即可**：拿不到输出，旧方法；
- **Popen 用到再学**：需要"启动后不等待"时才用；
- **安全底线**：列表传参，慎用 shell=True，绝不拼接不可信输入。
