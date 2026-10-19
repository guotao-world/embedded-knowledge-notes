# -*- coding: utf-8 -*-
"""
self 和 cls 里到底装的是什么？
—— 两个方法长得像，但"第一个参数收到的东西"级别完全不同。
"""

class Player:
    game = "RPG"                       # 类属性

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    # 实例方法：self 收到的是"一个具体的对象"
    def attack(self):
        print("self =", self)          # 看：是一个对象
        print("self.name =", self.name)
        self.hp += 10
        print(f"{self.name} attacks! HP now {self.hp}")

    # 类方法：cls 收到的是"类本身"
    @classmethod
    def get_game(cls):
        print("cls =", cls)            # 看：是一个类
        return cls.game

    # 类方法当"工厂"：用 cls 造新对象
    @classmethod
    def create(cls, name, hp):
        return cls(name, hp)


print("========== 1. self 里装的是什么 ==========")
p1 = Player("Alice", 100)
p1.attack()
# 输出会看到 self 是一个具体对象，还有自己的 name 属性

print("\n========== 2. cls 里装的是什么 ==========")
Player.get_game()
# 输出会看到 cls 是 <class '__main__.Player'>，是"类"本身

print("\n========== 3. 用对象调用类方法：装的还是类 ==========")
p1.get_game()
# 注意：cls 仍然收到 Player 类，不是 p1！
# 类方法不关心"是哪个对象在调"，它永远只拿到"类"

print("\n========== 4. 实例方法能用类名调用吗？ ==========")
try:
    Player.attack()                    # 不传对象 → 报错
except TypeError as e:
    print("Error:", e)
print(">>> 除非手动传对象：Player.attack(p1) —— 那就等于 p1.attack()")

print("\n========== 5. cls 能造对象，self 不能 ==========")
p2 = Player.create("Bob", 50)          # 通过类直接造对象，不用先 new
print("Created a new player:", p2.name, p2.hp)

print("\n========== 总结 ==========")
print("实例方法: self = 一个具体对象   → 读写这个对象的属性")
print("类方法:   cls = 类本身         → 读类属性、造新对象")
print("长得像，但里面装的货不同；名字 self/cls 就是提醒你装的什么。")
