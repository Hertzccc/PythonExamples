# coding: utf-8
# 场景类(墙、河流、树、冰)
import pygame
import random

# 地图由 石头墙24*24，钢墙24*24，冰12*12，河流12*12，树12*12等组成，分为不同的类，都继承小精灵类
# 石头墙


class Brick(pygame.sprite.Sprite):  # 图片大小为24 * 24
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.brick = pygame.image.load('./images/scene/brick.png')
        self.rect = self.brick.get_rect()
        self.being = False


# 钢墙
class Iron(pygame.sprite.Sprite):  # 图片大小为24 * 24
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.iron = pygame.image.load('./images/scene/iron.png')
        self.rect = self.iron.get_rect()
        self.being = False


# 冰
class Ice(pygame.sprite.Sprite):  # 图片大小为12 * 12
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ice = pygame.image.load('./images/scene/ice.png')
        self.rect = self.ice.get_rect()
        self.being = False


# 河流
class River(pygame.sprite.Sprite):  # 图片大小为12 * 12
    def __init__(self, kind=None):
        pygame.sprite.Sprite.__init__(self)
        if kind is None:
            self.kind = random.randint(0, 1)
        self.rivers = ['./images/scene/river1.png',
                       './images/scene/river2.png']
        self.river = pygame.image.load(self.rivers[self.kind])
        self.rect = self.river.get_rect()
        self.being = False


# 树
class Tree(pygame.sprite.Sprite):    # 12 * 12
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tree = pygame.image.load('./images/scene/tree.png')
        self.rect = self.tree.get_rect()
        self.being = False


# 地图
class Map():
    def __init__(self, stage):
        # 分组，便于碰撞检测
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.iceGroup = pygame.sprite.Group()
        self.riverGroup = pygame.sprite.Group()
        self.treeGroup = pygame.sprite.Group()
        # commented
        # if stage == 1:
        # 	self.stage1()
        # elif stage == 2:
        # 	self.stage2()
        self.set_stage(stage)
    #

    def set_stage(self, stage=1):  # 默认设置stage1
        self.stage1()
    # 关卡一

    def stage1(self):  # 630 * 630;    630 = 24 * 26 + 6 = 24 * 26 + 3 * 2 一排或一列能放 26个 brick
        # for x in [2, 3, 6, 7, 18, 19, 22, 23]:
        #     for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
        #         brick = Brick()
        #         brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        #         brick.being = True
        #         self.brickGroup.add(brick)
        # for x in [10, 11, 14, 15]:
        #     for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
        #         brick = Brick()
        #         brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        #         brick.being = True
        #         self.brickGroup.add(brick)

        # for x in [4, 5, 6, 7, 18, 19, 20, 21]:
        #     for y in [13, 14]:
        #         brick = Brick()
        #         brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        #         brick.being = True
        #         self.brickGroup.add(brick)
        # for x in [12, 13]:
        #     for y in [16, 17]:
        #         brick = Brick()
        #         brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        #         brick.being = True
        #         self.brickGroup.add(brick)
        # for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
        #     brick = Brick()
        #     brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        #     brick.being = True
        #     self.brickGroup.add(brick)

        # # 作弊模式: 司令部总是被钢板保护
        self.protect_home()

        # for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
        #     iron = Iron()
        #     iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
        #     iron.being = True
        #     self.ironGroup.add(iron)

        # 加自己的名字陈子豪 czh
        for x in [3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 18, 23]:
            for y in [1, 7]:
                tree = Tree()
                tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12
                tree.being = True
                self.treeGroup.add(tree)

        for x in [2, 6, 18, 23]:
            for y in [2, 6]:
                tree = Tree()
                tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12
                tree.being = True
                self.treeGroup.add(tree)

        for x in [1, 18, 23]:
            for y in [3, 5]:
                tree = Tree()
                tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12
                tree.being = True
                self.treeGroup.add(tree)

        for x in [1, 18, 19, 20, 21, 22, 23]:
            y = 4
            tree = Tree()
            tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12
            tree.being = True
            self.treeGroup.add(tree)

        for x in range(2, 7):
            for y in range(2, 7):
                if x + y == 8:
                    x += 8
                    # brick = Brick()
                    # brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
                    # brick.being = True
                    # self.brickGroup.add(brick)
                    tree = Tree()
                    tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12
                    tree.being = True
                    self.treeGroup.add(tree)
    # 关卡二

    def stage2(self):
        self.stage1()
        # for x in [2, 3, 6, 7, 18, 19, 22, 23]:
        # 	for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
        # 		brick = Brick()
        # 		brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        # 		brick.being = True
        # 		self.brickGroup.add(brick)
        # for x in [10, 11, 14, 15]:
        # 	for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
        # 		brick = Brick()
        # 		brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        # 		brick.being = True
        # 		self.brickGroup.add(brick)
        # for x in [4, 5, 6, 7, 18, 19, 20, 21]:
        # 	for y in [13, 14]:
        # 		brick = Brick()
        # 		brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        # 		brick.being = True
        # 		self.brickGroup.add(brick)
        # for x in [12, 13]:
        # 	for y in [16, 17]:
        # 		brick = Brick()
        # 		brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        # 		brick.being = True
        # 		self.brickGroup.add(brick)
        # for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
        # 	brick = Brick()
        # 	brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
        # 	brick.being = True
        # 	self.brickGroup.add(brick)
        # for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
        # 	iron = Iron()
        # 	iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
        # 	iron.being = True
        # 	self.ironGroup.add(iron)

    def protect_home(self):
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            iron = Iron()
            iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
            iron.being = True
            self.ironGroup.add(iron)
