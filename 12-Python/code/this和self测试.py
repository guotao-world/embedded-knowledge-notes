# -*- coding: utf-8 -*-
"""
测试：把 self 改叫 this，并且删掉第一个参数，会发生什么？
"""

print("--- Test 1: your code (this without self parameter) ---")

class Cat:
    # 你改成了这样：__init__(name, age)，没有第一个参数位置
    def __init__(name, age):
        this.name = name
        this.age = age

try:
    c1 = Cat("Mimi", 2)
    print(c1.name)
except Exception as e:
    print("Error type:", type(e).__name__)
    print("Error message:", e)

print("\n--- Test 2: keep a parameter slot, rename it to `this` ---")

class Cat2:
    def __init__(this, name, age):    # 第一个参数还在，只是改名 this
        this.name = name
        this.age = age

c2 = Cat2("Mimi", 2)
print("c2.name =", c2.name, "| c2.age =", c2.age)
print("Works! `this` is just another name for the object itself.")
