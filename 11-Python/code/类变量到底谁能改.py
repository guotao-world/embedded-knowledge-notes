# -*- coding: utf-8 -*-
"""
类变量到底谁能改？—— 不是只有 classmethod 能改！

结论先说：
1. 任何地方（实例方法、普通代码）都能改类变量 —— 只要通过"类名"改：Player.game = ...
2. 类方法里 cls.game = ... 是天然安全的写法（cls 就是类名）
3. 唯一的大坑：实例方法里写 self.game = ... 不是改类变量，
   而是给"这个对象"创建新属性，把类变量"盖住"了（遮蔽）。
"""

class Player:
    game = "RPG"                    # 类变量

    def __init__(self, name):
        self.name = name

    # ① 实例方法里"看似"改类变量 —— 实际是坑
    def wrong_try(self):
        self.game = "New Game"      # ❌ 这不是改类变量！
        print("  self.game   =", self.game)      # New Game（实例自己的）
        print("  Player.game =", Player.game)    # RPG（类变量没动！）

    # ② 实例方法里正确改法：通过类名
    def right_try(self):
        Player.game = "RPG2"        # ✅ 指名道姓改类变量
        print("  Player.game =", Player.game)

    # ③ 类方法：cls 就是类，天然安全
    @classmethod
    def change(cls):
        cls.game = "RPG3"           # ✅ cls.game 等价于 Player.game
        print("  Player.game =", Player.game)


print("========== 初始状态 ==========")
print("Player.game =", Player.game)             # RPG

print("\n========== ① 实例方法里写 self.game —— 陷阱 ==========")
p1 = Player("Alice")
p1.wrong_try()
print(">>> 类变量还是", Player.game, "—— self.game 只是给 p1 造了个新属性")

print("\n========== ② 实例方法通过类名改 —— 可以！ ==========")
p1.right_try()
p2 = Player("Bob")
print(">>> 新对象 p2 也看到:", p2.game, "—— 类变量真的变了，所有对象共用")
print(">>> 但注意：p1 自己的 game 还是 New Game —— 遮蔽的'盖子'不会自己消失")

print("\n========== ③ 类方法 cls.game 改 —— 可以！ ==========")
Player.change()
print(">>> 类变量现在是:", Player.game)

print("\n========== ④ 甚至类外面、普通代码也能改 ==========")
Player.game = "RPG4"               # 类定义之外直接改
print("Player.game =", Player.game)

print("\n========== 总结 ==========")
print("谁都能改类变量 —— 只要通过'类名'改（Player.game 或 cls.game）")
print("唯一不能做的是：实例方法里写 self.game = ...")
print("那不是修改，而是创建实例属性、遮蔽类变量。")
