# -*- coding: utf-8 -*-
"""
Python 模块与包 学习代码
（注释用中文，运行输出全部是英文）

第 1 节：为什么需要模块 —— 单文件 vs 多文件
第 2 节：导入标准库 import math / os
第 3 节：import 的四种姿势（含 from ... import * 的警告）
第 4 节：自建模块 —— import mymod
第 5 节：__name__ == "__main__" 是什么
第 6 节：包（package）—— mypkg/math_tools.py
第 7 节：pip —— 装第三方库的命令（在终端里敲）
第 8 节：venv —— 虚拟环境命令（在终端里敲）
第 9 节：综合小任务 —— os + 自建模块组合使用
"""

# ---------- 第 1 节：为什么需要模块 ----------
print("=" * 50)
print("Section 1: Why modules?")
print("=" * 50)

# 模块 = 把代码拆到不同文件里，用 import 互相引用
# 好处：代码好维护、可以复用、多人协作互不干扰
print("One file grows huge -> split into modules.")
print("A module is just a .py file. import brings it in.\n")

# ---------- 第 2 节：导入标准库 ----------
print("=" * 50)
print("Section 2: Import from the standard library")
print("=" * 50)

import math      # 导入整个模块，用"模块名.xxx"访问里面的东西
import os        # 操作系统相关功能

print(f"math.pi = {math.pi}")
print(f"math.sqrt(16) = {math.sqrt(16)}")
print(f"os.getcwd() = {os.getcwd()}\n")

# ---------- 第 3 节：import 的四种姿势 ----------
print("=" * 50)
print("Section 3: Four ways to import")
print("=" * 50)

# 姿势 1：import 模块 —— 之后用 模块名.函数 调用
import random
print(f"random.randint(1, 6) = {random.randint(1, 6)}")

# 姿势 2：from 模块 import 名字 —— 直接拿到函数，不用写模块名
from math import floor
print(f"floor(3.9) = {floor(3.9)}")

# 姿势 3：import 模块 as 别名 —— 名字太长或想改名时用
import datetime as dt
print(f"dt.date.today() = {dt.date.today()}")

# 姿势 4：from 模块 import * —— 全部导入，不推荐（名字冲突风险）
# 一般不这么写：会把模块里所有名字倒进来，可能覆盖你自己定义的变量
print("from math import * is possible but not recommended.\n")

# ---------- 第 4 节：自建模块 ----------
print("=" * 50)
print("Section 4: Import your own module (mymod.py)")
print("=" * 50)

# 自己写的 mymod.py 就在当前目录，直接 import（Python 优先找当前目录）
import mymod

print(f"mymod.PI = {mymod.PI}")
print(f"mymod.greet('Bob') = {mymod.greet('Bob')}")
print(f"mymod.double(21) = {mymod.double(21)}\n")

# ---------- 第 5 节：__name__ == "__main__" ----------
print("=" * 50)
print("Section 5: __name__ == '__main__'")
print("=" * 50)

# 每个 .py 文件都有一个内置变量 __name__：
# - 直接运行时，它是 "__main__"
# - 被 import 时，它是模块名（"mymod"）
# 所以 mymod.py 里 if __name__ == "__main__": 保护的那段测试代码，
# 在被 import 时不会执行 —— 上面我们 import mymod 时就没看到那两行输出
print(f"Running this file directly: __name__ = {__name__}")
print("mymod's test block did NOT run when imported.\n")

# ---------- 第 6 节：包（package） ----------
print("=" * 50)
print("Section 6: Package (mypkg/math_tools.py)")
print("=" * 50)

# 包 = 一个目录 + 若干模块，目录名就是包名
# 两种导入方式都行：
from mypkg import math_tools            # 方式 A：导入包里的模块
from mypkg.math_tools import add        # 方式 B：直接拿函数

print(f"math_tools.describe() = {math_tools.describe()}")
print(f"add(3, 4) = {add(3, 4)}\n")

# ---------- 第 7 节：pip ----------
print("=" * 50)
print("Section 7: pip - install third-party libraries")
print("=" * 50)
print("Run these in your terminal (NOT here):")
print("  pip install pyserial       # serial port library")
print("  pip install requests       # HTTP library")
print("  pip list                   # list installed packages")
print("  pip uninstall pyserial     # remove a package\n")

# ---------- 第 8 节：venv ----------
print("=" * 50)
print("Section 8: venv - virtual environment")
print("=" * 50)
print("Why: each project gets its own isolated libraries.")
print("Run these in your terminal (NOT here):")
print("  python -m venv myenv       # create a virtual env")
print("  myenv\\Scripts\\activate     # activate it (Windows)")
print("  pip install pyserial       # install INTO this env")
print("  deactivate                 # leave the env\n")

# ---------- 第 9 节：综合小任务 ----------
print("=" * 50)
print("Section 9: Mini task - combine os + mymod")
print("=" * 50)

# 小任务：给一批文件生成带编号的新文件名，演示模块组合使用
names = ["report", "log", "backup"]
for i, name in enumerate(names, 1):
    new_name = f"{i:02d}_{name}.txt"          # 01_report.txt 这种格式
    print(f"-> {new_name}  (double of {i} is {mymod.double(i)})")
print("Mini task done. Modules + stdlib work together!\n")

print("All sections finished. You know modules, packages, pip and venv!")
