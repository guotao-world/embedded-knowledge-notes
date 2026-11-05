# -*- coding: utf-8 -*-
"""
classmethod 改了类变量，下次实例化会用新值吗？—— 会！

更准确地说：类变量被改之后，从那一刻起，"整个类"都读到新值，
新实例化时 __init__ 会读取"当前"的类变量。

但已存在的旧实例要分两种情况：
- 当初把值"拷贝"进实例属性的 → 保持旧值（拷贝不会自动更新）
- 每次"动态读取"类变量的 → 立刻看到新值
"""

class Player:
    default_hp = 100                    # 类变量

    def __init__(self, name):
        self.name = name
        self.hp = Player.default_hp     # 实例化时读取"当前"值，拷贝一份给自己

    # 动态读取：每次调用都现场看类变量的当前值
    def show_default(self):
        print(f"    current default_hp = {Player.default_hp}")

    @classmethod
    def set_default_hp(cls, hp):
        cls.default_hp = hp


print("========== 1. 初始实例化 ==========")
p1 = Player("Alice")
print("p1.hp =", p1.hp)                 # 100

print("\n========== 2. classmethod 修改类变量 ==========")
Player.set_default_hp(200)
print("Player.default_hp =", Player.default_hp)   # 200

print("\n========== 3. 下次实例化：用新值！ ==========")
p2 = Player("Bob")
print("p2.hp =", p2.hp)                 # 200 ← 新实例用新值
p3 = Player("Cathy")
print("p3.hp =", p3.hp)                 # 200

print("\n========== 4. 已存在的旧实例：分两种情况 ==========")
print("p1.hp =", p1.hp)                 # 100 —— 旧实例当初拷贝了旧值，不变
print("p1 动态读取:", end=" ")
p1.show_default()                       # 200 —— 但现场读类变量时看到的是新值！

print("\n========== 5. 再改一次，继续验证 ==========")
Player.set_default_hp(300)
p4 = Player("David")
print("p4.hp =", p4.hp)                 # 300（新实例，新值）
print("p2.hp =", p2.hp)                 # 200（旧实例拷贝，保持 200）
print("p1 动态读取:", end=" ")
p1.show_default()                       # 300（动态读，跟到最新）

print("\n========== 总结 ==========")
print("1. 类变量被改后，新实例化一定用新值（__init__ 在实例化那一刻读取）")
print("2. 旧实例若把值拷贝进了实例属性 → 保持旧值")
print("3. 旧实例若每次都动态读类变量 → 也看到新值")
print("4. 类变量是'全类共享'的，修改影响从那一刻起的整个类")
