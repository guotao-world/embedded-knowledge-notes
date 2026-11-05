# -*- coding: utf-8 -*-
"""
Python 异常处理 + 文件读写 学习代码
（注释用中文，运行输出全部是英文）

第 1 节：为什么要异常处理 —— 不捕获的崩溃反例
第 2 节：try / except 基本用法
第 3 节：捕获指定异常 + 多个异常 + else / finally
第 4 节：常见内置异常一览
第 5 节：主动抛出异常 raise
第 6 节：写文件（with 自动关闭 + 追加模式）
第 7 节：读文件（读全部 / 读成行列表 / 逐行读）
第 8 节：综合小任务 —— 带异常保护的配置读取
"""

# ---------- 第 1 节：不捕获异常会怎样 ----------
print("=" * 50)
print("Section 1: What happens without try/except?")
print("=" * 50)


def dangerous_divide(a, b):
    # b 为 0 时，Python 会抛出一个 ZeroDivisionError
    return a / b


# 反例演示：这一行一旦执行，程序会当场崩溃并终止
# 想亲眼看崩溃？把下面这行的注释删掉再运行，程序会停在这里
# print(dangerous_divide(10, 0))
print("The crash line is disabled. Uncomment it to see a real crash.")
print("A crash = the whole program stops right there.\n")

# ---------- 第 2 节：try / except 基本用法 ----------
print("=" * 50)
print("Section 2: try / except basics")
print("=" * 50)

try:
    result = dangerous_divide(10, 0)   # 这一行会抛出异常
except ZeroDivisionError:
    result = None
    print("Caught ZeroDivisionError: cannot divide by zero.")

# 捕获之后，程序不会停，继续往下走
print("Program continues to run after the error.\n")

# ---------- 第 3 节：捕获指定异常 + 多异常 + else / finally ----------
print("=" * 50)
print("Section 3: specific errors, multiple errors, else and finally")
print("=" * 50)


def parse_number(text):
    # 传进来的不是数字时，int() 会抛 ValueError
    return int(text)


try:
    parse_number("abc")
except ValueError:
    print("Caught ValueError: 'abc' is not a number.")
except TypeError:
    print("Caught TypeError.")
else:
    # else：只有没出错时才执行
    print("No error happened (else block).")
finally:
    # finally：无论出错与否都执行，常用于收尾（关闭资源）
    print("finally always runs, error or not.\n")

# ---------- 第 4 节：常见内置异常一览 ----------
print("=" * 50)
print("Section 4: common built-in exceptions")
print("=" * 50)

try:
    open("no_such_file.txt")            # 文件不存在 -> FileNotFoundError
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

try:
    [1, 2, 3][10]                       # 下标越界 -> IndexError
except IndexError as e:
    print(f"IndexError: {e}")

try:
    {"a": 1}["b"]                       # 键不存在 -> KeyError
except KeyError as e:
    print(f"KeyError: {e}")

try:
    "1" + 1                             # 类型不匹配 -> TypeError
except TypeError as e:
    print(f"TypeError: {e}")
print()

# ---------- 第 5 节：主动抛出异常 raise ----------
print("=" * 50)
print("Section 5: raise your own error")
print("=" * 50)


def check_age(age):
    if age < 0 or age > 150:
        # 主动抛出一个错误，让调用方知道"参数不合法"
        raise ValueError(f"age {age} is out of range 0-150")
    return f"age {age} is valid"


try:
    check_age(200)
except ValueError as e:
    print(f"Raised and caught: {e}\n")

# ---------- 第 6 节：写文件（with 自动关闭） ----------
print("=" * 50)
print("Section 6: writing files with `with`")
print("=" * 50)

# with 语句会在代码块结束时自动关闭文件，不用手动 close()，也不怕忘
# 模式 'w' = 覆盖写入；'a' = 追加写入；不写模式默认是 'r' 只读
with open("demo_note.txt", "w", encoding="utf-8") as f:
    f.write("Hello from Python!\n")
    f.write("Line 2: learning file I/O.\n")

with open("demo_note.txt", "a", encoding="utf-8") as f:
    f.write("Line 3: appended by 'a' mode.\n")
print("demo_note.txt written (overwrite + append).\n")

# ---------- 第 7 节：读文件 ----------
print("=" * 50)
print("Section 7: reading files")
print("=" * 50)

with open("demo_note.txt", "r", encoding="utf-8") as f:
    whole = f.read()                    # 一次性读全部内容
print("--- read() ---")
print(whole)

with open("demo_note.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()               # 读成"每行一个元素"的列表
print("--- readlines() ---")
for i, line in enumerate(lines, 1):
    print(f"line {i}: {line.rstrip()}")   # rstrip() 去掉末尾的换行符

with open("demo_note.txt", "r", encoding="utf-8") as f:
    # 逐行读：大文件推荐写法，一次只占一行内存
    print("--- for line in f: read line by line ---")
    for line in f:
        print(line.rstrip())
print()

# ---------- 第 8 节：综合小任务（异常保护 + 文件读写） ----------
print("=" * 50)
print("Section 8: mini task - safe config loading with error log")
print("=" * 50)


def load_config(file_path, default_name="unknown"):
    """读一个两行格式的配置文件：第一行是名字，第二行是端口号。

    文件不存在、行数不够、端口不是数字 —— 三种情况都不崩溃，返回默认值。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        name = lines[0].strip()
        port = int(lines[1].strip())
        return {"name": name, "port": port}
    except FileNotFoundError:
        # 文件不存在 -> 用默认值顶上
        return {"name": default_name, "port": 0}
    except (IndexError, ValueError):
        # 行数不够（IndexError）或端口不是数字（ValueError）-> 也用默认值
        return {"name": default_name, "port": 0}


# 故意读一个不存在的文件，看它怎么"安全地"失败
config = load_config("no_such_config.txt")
print(f"Missing config -> {config}")

# 再写一个正常配置文件，读出来
with open("my_config.txt", "w", encoding="utf-8") as f:
    f.write("rk3568-device\n")
    f.write("8080\n")
config = load_config("my_config.txt")
print(f"Good config   -> {config}\n")

print("All sections finished. Now you know try/except + file I/O!")
