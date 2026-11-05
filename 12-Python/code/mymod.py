# -*- coding: utf-8 -*-
"""
自建模块：被 Python模块与包学习代码.py 导入演示用
也可以单独运行：python mymod.py
"""

PI = 3.14159          # 模块级变量（被 import 后可通过 mymod.PI 访问）


def greet(name):
    """一个简单的打招呼函数"""
    return f"Hello, {name}! from mymod"


def double(x):
    """返回两倍"""
    return x * 2


if __name__ == "__main__":
    # 直接运行 python mymod.py 时才会执行这里
    # 被 import 时不会执行 —— 这就是 __name__ 的用途
    print("mymod.py is being run directly.")
    print(greet("standalone"))
