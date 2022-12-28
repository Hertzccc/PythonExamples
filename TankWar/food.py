# coding: utf-8
# 食物类
import pygame
import random


# 食物类, 用于提升坦克能力
class Food(pygame.sprite.Sprite):
    def __init__(self):
        # 先调用父类构造方法
        pygame.sprite.Sprite.__init__(self)
        # a消灭当前所有敌人
        self.food_bomb = './images/food/food_bomb.png'
        # a当前所有敌人静止一段时间
        self.food_clock = './images/food/food_clock.png'
        # 使得坦克子弹可碎钢板
        self.food_gun = './images/food/food_gun.png'
        # a使得大本营的墙变为钢板
        # self.food_iron = './images/food/food_gun.png'    # BUG
        self.food_iron = './images/food/food_iron.png'
        # a坦克获得一段时间的保护罩
        self.food_protect = './images/food/food_protect.png'
        # a坦克升级
        self.food_star = './images/food/food_star.png'
        # a坦克生命+1
        self.food_tank = './images/food/food_tank.png'
        # 所有食物
        self.foods = [self.food_bomb, self.food_clock, self.food_gun,
                      self.food_iron, self.food_protect, self.food_star, self.food_tank]
        # 暂时设为None, 在调用generate()时, 随机生成一种food，初始化
        self.kind = None
        self.food = None
        self.rect = None
        # 是否存在
        self.being = False
        # 存在时间
        self.time = 1000

    # 生成食物
    def generate(self):
        self.kind = random.randint(0, 6) #随机食物0~6
		# convert_alpha()方法会使用透明的方法绘制前景对象，因此在加载一个有alpha通道的素材时（比如PNG TGA），需要使用convert_alpha()方法
        self.food = pygame.image.load(self.foods[self.kind]).convert_alpha()
        self.rect = self.food.get_rect()
        self.rect.left, self.rect.top = random.randint(
            100, 500), random.randint(100, 500)
        self.being = True #存活
