# -*- coding: utf-8 -*-
"""
怎么判断类里的方法要不要 self？
不用 self 的类内函数，必须加 @staticmethod 吗？
—— 必须！（要么 @staticmethod，要么 @classmethod，不能裸着）

本文件把三种情况放在同一个类里对照，最后还有一个故意写错的反例。
"""

# ============================================================
# 一个类里同时放三种方法，对照着看
# ============================================================
class Player:
    game = "RPG"                       # 类属性：所有玩家共用

    def __init__(self, name, hp):
        self.name = name               # 实例属性：每个玩家自己的
        self.hp = hp

    # ① 实例方法：方法体里用了 self.name / self.hp
    #    判断标准：要用"这个对象自己的数据" → 必须写 self
    def attack(self):
        self.hp += 10
        print(f"{self.name} attacks! HP now {self.hp}")

    # ② 类方法：方法体里没用 self.xxx，但用了类属性 game
    #    判断标准：要用"整个类共用的数据" → @classmethod + cls
    @classmethod
    def get_game(cls):
        return cls.game

    # ③ 静态方法：谁的数据都不用，输入输出全靠参数
    #    判断标准：什么都不碰 → @staticmethod，不写 self
    @staticmethod
    def is_valid_hp(hp):
        return hp >= 0

    @staticmethod
    def version():
        return "v1.0"


print("========== Three methods in one class ==========")
p1 = Player("Alice", 100)
p1.attack()                          # 实例方法：self = p1
print("Game name:", Player.get_game())     # 类方法：cls = Player
print("HP valid?", Player.is_valid_hp(-5)) # 静态方法：谁都不进
print("Version:", Player.version())

# ============================================================
# 反例：不加 self，也不加 @staticmethod —— 会怎样？
# ============================================================
print("\n========== Wrong example: no self, no decorator ==========")

class Wrong:
    def hello():                     # ❌ 两个都没有
        print("I am a bare function in a class")

# 用"对象.方法()"调用 → 报错！
print("--- Call via instance (will crash) ---")
try:
    w = Wrong()
    w.hello()
except TypeError as e:
    print("Error type:", type(e).__name__)
    print("Error message:", e)
    print(">> Reason: Python 自动把 w 塞给了第一个参数，")
    print("   但 hello() 没留参数位，装不下。")

# 用"类名.方法()"调用 → 能跑，但这不是正常方法用法
print("\n--- Call via class (works, but weird) ---")
Wrong.hello()
print(">> 同一个函数，两种调用方式行为不一样，很容易踩坑，")
print("   所以类里的函数：要么写 self，要么加装饰器，不能裸着。")

# ============================================================
# 判断流程图（背下来）
# ============================================================
print("\n========== How to decide (2 questions) ==========")
print("Q1: 方法体里用 self.xxx 吗？(要碰对象自己的数据)")
print("    YES -> 实例方法，第一个参数写 self")
print("Q2: NO -> 用类共用的数据吗？(比如类属性)")
print("    YES -> 类方法，@classmethod，第一个参数写 cls")
print("    NO  -> 静态方法，@staticmethod，不写 self")
print("注意：不用 self 的函数在类里不能裸着，")
print("      必须 @staticmethod 或 @classmethod 二选一。")
