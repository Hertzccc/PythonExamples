# coding: utf-8
# 坦克类
import pygame
import random
from bullet import Bullet


# 我方坦克类
class myTank(pygame.sprite.Sprite):  # 48 * 48
    MAX_DIR_CHANGE_CACHE_CNT = 5

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        # 玩家编号(1/2)
        self.player = player
        # 不同玩家用不同的坦克(不同等级对应不同的图)
        if player == 1:
            self.tanks = ['./images/myTank/tank_T1_0.png',
                          './images/myTank/tank_T1_1.png', './images/myTank/tank_T1_2.png']
        elif player == 2:
            self.tanks = ['./images/myTank/tank_T2_0.png',
                          './images/myTank/tank_T2_1.png', './images/myTank/tank_T2_2.png']
        else:
            raise ValueError('myTank class -> player value error.')
        # 坦克等级(初始0)
        self.level = 0
        # 载入(两个tank是为了轮子特效, 因为两张tank图片的轮子履带处不同, 交替显示时, 会有履带在转动的效果)
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        # 保护罩,  96*48的图片
        self.protected_mask = pygame.image.load(
            './images/others/protect.png').convert_alpha()
        self.protected_mask1 = self.protected_mask.subsurface((0, 0), (48, 48))
        self.protected_mask2 = self.protected_mask.subsurface(
            (48, 0), (48, 48))
        # 坦克方向, 默认向上
        self.direction_x, self.direction_y = 0, -1
        # 不同玩家的出生位置不同
        if player == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        elif player == 2:
            self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
        else:
            raise ValueError('myTank class -> player value error.')
        # 坦克速度
        self.speed = 3
        # 是否存活
        self.being = True
        # 有几条命
        self.life = 3
        # 是否处于保护状态, 把此变量设为True, 可进入作弊模式, 让我方坦克处于防弹状态
        # 问题（4） 答案： 这个变量 self.protected = True 即可进入作弊
        self.protected = False
        # 子弹
        self.bullet = Bullet()

    # 射击
    def shoot(self):
        # 在发出去的一发子弹, 没有到达边界以前, 不能再次发射
        self.bullet.being = True
        stronger = self.bullet.stronger
        # 根据坦克的当前朝向和位置, 设置子弹的方向和位置, 子弹出现在坦克前方不远处
        self.bullet.turn(self.direction_x, self.direction_y)
        if self.direction_x == 0 and self.direction_y == -1:   # UP
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:  # DOWN
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:  # LEFT
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:   # RIGHT
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('myTank class -> direction value error.')
        # 坦克的等级提升后, 子弹的速度会加快, 提到2级及以上等级后, 可碎钢板
        if self.level == 0:
            self.bullet.speed = 8
            self.bullet.stronger = False
        elif self.level == 1:
            self.bullet.speed = 12
            self.bullet.stronger = False
        elif self.level == 2:
            self.bullet.speed = 12
            self.bullet.stronger = True
        elif self.level == 3:     # BUG, 图片只提供了0到2级的, 没有3级坦克的图片
            self.bullet.speed = 16
            self.bullet.stronger = True
        else:
            raise ValueError('myTank class -> level value error.')
        # added, 2021.01.16
        if stronger:
            self.bullet.stronger = stronger

    # 等级提升
    def up_level(self):
        # if self.level < 3:    # Bug
        if self.level < 2:
            self.level += 1
        try:
            self.tank = pygame.image.load(
                self.tanks[self.level]).convert_alpha()
        except:
            self.tank = pygame.image.load(self.tanks[-1]).convert_alpha()

    # 等级降低
    def down_level(self):
        if self.level > 0:
            self.level -= 1
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()

    # 尝试沿坦克的朝向移动
    def try_move(self):
        self.rect = self.rect.move(
            self.speed * self.direction_x, self.speed * self.direction_y)

    # 撤销移动(通过反向移动来实现)
    def undo_move(self):
        self.rect = self.rect.move(
            self.speed * -self.direction_x, self.speed * -self.direction_y)

    def detect_and_undo(self, tankGroup, brickGroup, ironGroup, myhome):
        # 是否可以移动
        is_move = True
        # 判断是否超出地图四个边界, 及是否与砖墙, 钢墙, 其他坦克及大本营碰撞
        if self.rect.top < 3 or self.rect.bottom > 630 - 3 or \
                self.rect.left < 3 or self.rect.right > 630 - 3 or \
                pygame.sprite.spritecollide(self, brickGroup, False, None) or \
                pygame.sprite.spritecollide(self, ironGroup, False, None) or  \
                pygame.sprite.spritecollide(self, tankGroup, False, None) or \
                pygame.sprite.collide_rect(self, myhome):
            self.undo_move()
            is_move = False
        return is_move

    def do_move(self, tankGroup, brickGroup, ironGroup, myhome, dx, dy, x0y0, w0h0, x1y1, w1h1):
        # 改变朝向
        self.direction_x, self.direction_y = dx, dy
        # 根据朝向, 重新设置坦克外观
        self.tank_0 = self.tank.subsurface(x0y0, w0h0)
        self.tank_1 = self.tank.subsurface(x1y1, w1h1)
        # 先移动后判断
        self.try_move()
        return self.detect_and_undo(tankGroup, brickGroup, ironGroup, myhome)

    # 向上

    def move_up(self, tankGroup, brickGroup, ironGroup, myhome):
        return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
                            0, -1,
                            (0, 0), (48, 48),
                            (48, 0), (48, 48))

    # 向下
    def move_down(self, tankGroup, brickGroup, ironGroup, myhome):
        return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
                            0, 1,
                            (0, 48), (48, 48),
                            (48, 48), (48, 48))

    # 向左
    def move_left(self, tankGroup, brickGroup, ironGroup, myhome):
        return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
                            -1, 0,
                            (0, 96), (48, 48),
                            (48, 96), (48, 48))

    # 向右
    def move_right(self, tankGroup, brickGroup, ironGroup, myhome):
        return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
                            1, 0,
                            (0, 144), (48, 48),
                            (48, 144), (48, 48))

    # 死后重置, 我方坦克挂掉后, 重新复位
    def reset(self):
        self.level = 0
        self.protected = False
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        # 默认的坦克朝向为向上
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        self.direction_x, self.direction_y = 0, -1
        # 给不同的玩家不同的初始位置
        if self.player == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        elif self.player == 2:
            self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
        else:
            raise ValueError('myTank class -> player value error.')
        self.speed = 3
        # 重置炮弹
        self.bullet.stronger = False


# 敌方坦克类
class enemyTank(pygame.sprite.Sprite):
    def __init__(self, x=None, kind=None, is_red=None):
        pygame.sprite.Sprite.__init__(self)
        # 用于给刚生成的坦克播放出生特效
        self.born = True
        # 90个滴答? 根据tick()函数来决定真正所需的时间, 如果tick(60), 即每秒60个滴答(界面刷新), 则出生特效大概需要1.5秒
        self.times = 90
        # 敌方坦克的种类编号: 从0到3
        if kind is None:
            self.kind = random.randint(0, 3)
        else:
            self.kind = kind
        # 所有敌方坦克: 共有4种kind, 同一kind, 内部也分为4种不同的颜色
        self.tanks1 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png',
                       './images/enemyTank/enemy_1_2.png', './images/enemyTank/enemy_1_3.png']
        self.tanks2 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png',
                       './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png']
        self.tanks3 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png',
                       './images/enemyTank/enemy_3_2.png', './images/enemyTank/enemy_3_3.png']
        self.tanks4 = ['./images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_1.png',
                       './images/enemyTank/enemy_4_2.png', './images/enemyTank/enemy_4_3.png']
        self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
        # 是否携带食物(红色的坦克携带食物)
        if is_red is None:
            self.is_red = random.choice((True, False, False, False, False))
        else:
            self.is_red = is_red
        # added
        #self.is_red = True
        # 同一种类的坦克具有不同的颜色, 红色的坦克比同类坦克多一点血量
        if self.is_red:
            self.color = 3
        else:
            self.color = random.randint(0, 2)
        # 血量
        self.blood = self.color
        # self.tank对应的图片(96*192), 包含了8张坦克(48*48)的外观
        self.tank = pygame.image.load(
            self.tanks[self.kind][self.color]).convert_alpha()
        # 两个tank是为了轮子特效
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_0.get_rect()
        # 坦克位置:  最顶部的左, 中和右三个位置, 随机出现敌方坦克
        if x is None:
            self.x = random.randint(0, 2)
        else:
            self.x = x
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
        # 坦克是否可以行动
        self.can_move = True
        # 坦克速度
        self.speed = max(3 - self.kind, 1)
        # 方向
        self.direction_x, self.direction_y = 0, 1
        # 是否存活
        self.being = True
        # 子弹
        self.bullet = Bullet()
    # 射击

    def shoot(self):
        self.bullet.being = True
        self.bullet.turn(self.direction_x, self.direction_y)
        if self.direction_x == 0 and self.direction_y == -1:     # UP
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:    # DOWN
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:   # LEFT
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:    # RIGHT
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('enemyTank class -> direction value error.')

    # 尝试沿坦克的朝向移动
    def try_move(self):
        self.rect = self.rect.move(
            self.speed * self.direction_x, self.speed * self.direction_y)

    # 撤销移动(通过反向移动来实现)
    def undo_move(self):
        self.rect = self.rect.move(
            self.speed * -self.direction_x, self.speed * -self.direction_y)

    # 生成随机方向
    def random_direction(self):
        self.direction_x, self.direction_y = random.choice(
            ([0, 1], [0, -1], [1, 0], [-1, 0]))

    # 随机移动
    def move(self, tankGroup, brickGroup, ironGroup, myhome):
        # 1%的概率, 随机改变运动方向
        if random.randint(0, 99) == 0:
            self.random_direction()
        # 根据坦克当前朝向, 设置其外观, self.tank对应的图片(96*192), 包含了8张坦克(48*48)的外观
        if self.direction_x == 0 and self.direction_y == -1:        # UP
            self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        elif self.direction_x == 0 and self.direction_y == 1:       # DOWN
            self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        elif self.direction_x == -1 and self.direction_y == 0:      # LEFT
            self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
        elif self.direction_x == 1 and self.direction_y == 0:       # RIGHT
            self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
        else:
            raise ValueError('enemyTank class -> direction value error.')
        # 先移动后判断
        self.try_move()
        is_move = True
        # 判断是否超出地图四个边界, 及是否与砖墙, 钢墙, 其他坦克及大本营碰撞
        if self.rect.top < 3 or self.rect.bottom > 630 - 3 or \
                self.rect.left < 3 or self.rect.right > 630 - 3 or \
                pygame.sprite.spritecollide(self, brickGroup, False, None) or \
                pygame.sprite.spritecollide(self, ironGroup, False, None) or  \
                pygame.sprite.spritecollide(self, tankGroup, False, None) or \
                pygame.sprite.collide_rect(self, myhome):
            # 撤销刚才尝试做出的移动
            self.undo_move()
            # 随机产生新的运动方向
            self.random_direction()
            is_move = False
        return is_move

    # 重新载入坦克外观图片, 因为敌方坦克被击中后, 血量变少, 颜色也要改变
    def reload(self):
        self.tank = pygame.image.load(
            self.tanks[self.kind][self.color]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
