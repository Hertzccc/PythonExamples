# coding: utf-8
# 游戏运行主程序
import sys
import pygame
import scene
import bullet
import food
import tanks
import home
from pygame.locals import *


is_gameover = False
NUM_OF_STAGES = 3


# 开始界面显示
def show_start_interface(screen, width, height):
    tfont = pygame.font.Font('./font/simkai.ttf', width//4)
    cfont = pygame.font.Font('./font/simkai.ttf', width//20)
    title = tfont.render(u'坦克大战', True, (255, 0, 0))
    content1 = cfont.render(u'按1键进入单人游戏', True, (0, 0, 255))
    content2 = cfont.render(u'按2键进入双人人游戏', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (width/2, height/4)
    crect1 = content1.get_rect()
    crect1.midtop = (width/2, height/1.8)
    crect2 = content2.get_rect()
    crect2.midtop = (width/2, height/1.6)
    screen.blit(title, trect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2


# 结束界面显示
def show_end_interface(screen, width, height, is_win):
    bg_img = pygame.image.load("./images/others/background.png")   # 630 * 630
    screen.blit(bg_img, (0, 0))
    if is_win:
        font = pygame.font.Font('./font/simkai.ttf', width//10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(content, rect)
    else:
        fail_img = pygame.image.load("./images/others/gameover.png")  # 64 * 32
        rect = fail_img.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(fail_img, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


# 关卡切换
def show_switch_stage(screen, width, height, stage):
    bg_img = pygame.image.load("./images/others/background.png")
    screen.blit(bg_img, (0, 0))
    font = pygame.font.Font('./font/simkai.ttf', width//10)
    content = font.render(u'第%d关' % stage, True, (0, 255, 0))
    rect = content.get_rect()
    rect.midtop = (width/2, height/2)
    screen.blit(content, rect)
    pygame.display.update()
    delay_event = pygame.constants.USEREVENT + 3
    pygame.time.set_timer(delay_event, 1000, loops=1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == delay_event:
                return


# 我方坦克
def handle_mytanksGroup(stage_data, screen):
    if stage_data.tank_player1 in stage_data.mytanksGroup:
        # 当玩家按下方向键, 即坦克在移动时, 通过切换两张不同的外观, 来显示坦克履带的运动的特效
        if stage_data.is_switch_tank and stage_data.player1_moving:
            screen.blit(stage_data.tank_player1.tank_0,
                        (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
            stage_data.player1_moving = False
        else:
            screen.blit(stage_data.tank_player1.tank_1,
                        (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
        if stage_data.tank_player1.protected:
            screen.blit(stage_data.tank_player1.protected_mask1,
                        (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
    if stage_data.num_player > 1:
        if stage_data.tank_player2 in stage_data.mytanksGroup:
            if stage_data.is_switch_tank and stage_data.player2_moving:
                screen.blit(stage_data.tank_player2.tank_0,
                            (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))
                # player1_moving = False  # BUG
                stage_data.player2_moving = False
            else:
                screen.blit(stage_data.tank_player2.tank_1,
                            (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))
            if stage_data.tank_player2.protected:
                screen.blit(stage_data.tank_player1.protected_mask1,
                            (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))


# 敌方坦克
def handle_enemytanksGroup(stage_data, screen):
    for each in stage_data.enemytanksGroup:
        # 出生特效
        if each.born:
            if each.times > 0:
                each.times -= 1
                # 星星从小到大有3张图片, 每10个滴答改变一次外观, 90个滴答内, 共可显示3遍从小到大变化的特效
                if each.times <= 10:
                    screen.blit(
                        stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
                elif each.times <= 20:
                    screen.blit(
                        stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
                elif each.times <= 30:
                    screen.blit(
                        stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
                elif each.times <= 40:
                    screen.blit(
                        stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
                elif each.times <= 50:
                    screen.blit(
                        stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
                elif each.times <= 60:
                    screen.blit(
                        stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
                elif each.times <= 70:
                    screen.blit(
                        stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
                elif each.times <= 80:
                    screen.blit(
                        stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
                elif each.times <= 90:
                    screen.blit(
                        stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
            else:
                # 出生特效状态结束
                each.born = False
        else:
            # 只有在允许敌方坦克移动时, 才改变其方位
            if each.can_move:
                stage_data.tanksGroup.remove(each)
                each.move(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                          stage_data.map_stage.ironGroup, stage_data.myhome)
                stage_data.tanksGroup.add(each)
            # 敌方坦克, 始终显示履带特效, 即使被food_clock给静止后, 履带仍然在原地打转
            if stage_data.is_switch_tank:
                screen.blit(each.tank_0, (each.rect.left, each.rect.top))
            else:
                screen.blit(each.tank_1, (each.rect.left, each.rect.top))


# 我方子弹
def handle_mybullet(stage_data, sound_data, screen):
    global is_gameover
    for tank_player in stage_data.mytanksGroup:
        if tank_player.bullet.being:
            # 改变当前坦克的炮弹的位置, 然后重新绘制
            tank_player.bullet.move()
            screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
            # 子弹碰撞敌方子弹
            for each in stage_data.enemybulletsGroup:
                if each.being:
                    if pygame.sprite.collide_rect(tank_player.bullet, each):
                        tank_player.bullet.being = False
                        each.being = False
                        stage_data.enemybulletsGroup.remove(each)
                        break
                else:
                    stage_data.enemybulletsGroup.remove(each)
            # 子弹碰撞敌方坦克
            for each in stage_data.enemytanksGroup:
                if each.being:
                    if pygame.sprite.collide_rect(tank_player.bullet, each):
                        # 红色坦克被击中后, 会随机产生奖励
                        if each.is_red:
                            myfood = food.Food()
                            myfood.generate()
                            stage_data.myfoodsGroup.add(myfood)
                            each.is_red = False
                        # 敌方坦克被击中后, 血量变少, 坦克颜色也随之改变
                        each.blood -= 1
                        each.color -= 1
                        if each.blood < 0:
                            sound_data.bang_sound.play()
                            each.being = False
                            stage_data.enemytanksGroup.remove(each)
                            stage_data.enemytanks_now -= 1
                            stage_data.tanksGroup.remove(each)
                        else:
                            each.reload()
                        tank_player.bullet.being = False
                        break
                else:
                    stage_data.enemytanksGroup.remove(each)
                    stage_data.tanksGroup.remove(each)
            # 子弹碰撞石头墙
            if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.brickGroup, True, None):
                tank_player.bullet.being = False

            # 子弹碰钢墙
            if tank_player.bullet.stronger:
                if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.ironGroup, True, None):
                    tank_player.bullet.being = False
            else:
                if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.ironGroup, False, None):
                    tank_player.bullet.being = False

            # 子弹碰大本营
            if pygame.sprite.collide_rect(tank_player.bullet, stage_data.myhome):
                tank_player.bullet.being = False
                stage_data.myhome.set_dead()
                is_gameover = True


# 敌方子弹
def handle_enemy_bullet(stage_data, sound_data, screen):
    global is_gameover
    # for each in stage_data.enemytanksGroup:
    #     if each.being:
    #         # 敌方坦克可移动, 且未开火
    #         if each.can_move and not each.bullet.being:
    #             stage_data.enemybulletsGroup.remove(each.bullet)
    #             # 敌方坦克开火, 将其炮弹的being设为True
    #             each.shoot()
    #             stage_data.enemybulletsGroup.add(each.bullet)
    #         # 敌方坦克不是处于出生特效状态
    #         if not each.born:
    #             if each.bullet.being:
    #                 # 敌方子弹往前飞行, 更新位置后, 再重绘
    #                 each.bullet.move()
    #                 screen.blit(each.bullet.bullet, each.bullet.rect)
    #                 # 子弹碰撞我方坦克
    #                 for tank_player in stage_data.mytanksGroup:
    #                     if pygame.sprite.collide_rect(each.bullet, tank_player):
    #                         # 若坦克没有防护罩
    #                         if not tank_player.protected:
    #                             sound_data.bang_sound.play()
    #                             tank_player.life -= 1
    #                             if tank_player.life < 0:
    #                                 stage_data.mytanksGroup.remove(tank_player)
    #                                 stage_data.tanksGroup.remove(tank_player)
    #                                 # 当双打时, 两个玩家中, 可能还有一个玩家仍然没有挂掉
    #                                 # 只有两个玩家都挂掉后, 才game over
    #                                 if len(stage_data.mytanksGroup) < 1:
    #                                     is_gameover = True
    #                             else:
    #                                 # 当还有可用坦克时, 重新复位一下当前玩家的坦克
    #                                 tank_player.reset()
    #                         each.bullet.being = False
    #                         stage_data.enemybulletsGroup.remove(each.bullet)
    #                         break
    #                 # 子弹碰撞石头墙
    #                 if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.brickGroup, True, None):
    #                     each.bullet.being = False
    #                     stage_data.enemybulletsGroup.remove(each.bullet)

    #                 # 子弹碰钢墙
    #                 if each.bullet.stronger:
    #                     if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.ironGroup, True, None):
    #                         each.bullet.being = False
    #                         # added, 2022.01.15
    #                         stage_data.enemybulletsGroup.remove(each.bullet)
    #                 else:
    #                     if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.ironGroup, False, None):
    #                         # added, 2022.01.15
    #                         each.bullet.being = False
    #                         stage_data.enemybulletsGroup.remove(each.bullet)

    #                 # 子弹碰大本营
    #                 if pygame.sprite.collide_rect(each.bullet, stage_data.myhome):
    #                     each.bullet.being = False
    #                     stage_data.myhome.set_dead()
    #                     is_gameover = True
    # else:
    #     stage_data.enemytanksGroup.remove(each)
    #     stage_data.tanksGroup.remove(each)


def handle_food(stage_data, sound_data, screen):
    for myfood in stage_data.myfoodsGroup:
        if myfood.being and myfood.time > 0:
            screen.blit(myfood.food, myfood.rect)
            myfood.time -= 1
            for tank_player in stage_data.mytanksGroup:
                # 当玩家的坦克碰到food时
                if pygame.sprite.collide_rect(tank_player, myfood):
                    # 消灭当前所有敌人
                    if myfood.kind == 0:
                        for t in stage_data.enemytanksGroup:
                            sound_data.bang_sound.play()
                            # added, 2022.01.16
                            stage_data.tanksGroup.remove(t)
                        # 清空enemyTanksGroup中的所有坦克
                        stage_data.enemytanksGroup = pygame.sprite.Group()
                        # BUG. Commented 2022.01.16
                        #stage_data.enemytanks_total -= stage_data.enemytanks_now
                        stage_data.enemytanks_now = 0
                    # 敌人静止
                    if myfood.kind == 1:
                        sound_data.add_sound.play()
                        for each in stage_data.enemytanksGroup:
                            each.can_move = False
                        pygame.time.set_timer(
                            stage_data.recoverEnemyEvent, 8000, loops=1)
                    # 子弹增强
                    if myfood.kind == 2:
                        sound_data.add_sound.play()
                        # 原代码未起作用, 会在myTank.shoot()中被改写; 要修改myTank.shoot()
                        tank_player.bullet.stronger = True
                    # 使得大本营的墙变为钢板
                    if myfood.kind == 3:
                        stage_data.map_stage.protect_home()
                    # 坦克获得一段时间的保护罩
                    if myfood.kind == 4:
                        sound_data.add_sound.play()
                        for t in stage_data.mytanksGroup:
                            t.protected = True
                        pygame.time.set_timer(
                            stage_data.noprotectMytankEvent, 8000, loops=1)
                    # 坦克升级
                    if myfood.kind == 5:
                        sound_data.add_sound.play()
                        tank_player.up_level()
                    # 坦克生命+1
                    if myfood.kind == 6:
                        sound_data.add_sound.play()
                        tank_player.life += 1
                    myfood.being = False
                    stage_data.myfoodsGroup.remove(myfood)
                    # break
        else:
            myfood.being = False
            stage_data.myfoodsGroup.remove(myfood)


# 处理玩家一的相关按键事件
# WSAD -> 上下左右
# 空格键射击
def handle_player1_events(key_pressed, sound_data, stage_data):
    # 用户只要有按住方向键, 则认为tank处于moving状态, 所以设置player1_moving为true
    if key_pressed[pygame.K_w]:
        stage_data.tanksGroup.remove(stage_data.tank_player1)
        stage_data.tank_player1.move_up(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                        stage_data.map_stage.ironGroup, stage_data.myhome)
        stage_data.tanksGroup.add(stage_data.tank_player1)
        stage_data.player1_moving = True
    elif key_pressed[pygame.K_s]:
        stage_data.tanksGroup.remove(stage_data.tank_player1)
        stage_data.tank_player1.move_down(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                          stage_data.map_stage.ironGroup, stage_data.myhome)
        stage_data.tanksGroup.add(stage_data.tank_player1)
        stage_data.player1_moving = True
    elif key_pressed[pygame.K_a]:
        stage_data.tanksGroup.remove(stage_data.tank_player1)
        stage_data.tank_player1.move_left(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                          stage_data.map_stage.ironGroup, stage_data.myhome)
        stage_data.tanksGroup.add(stage_data.tank_player1)
        stage_data.player1_moving = True
    elif key_pressed[pygame.K_d]:
        stage_data.tanksGroup.remove(stage_data.tank_player1)
        stage_data.tank_player1.move_right(
            stage_data.tanksGroup, stage_data.map_stage.brickGroup, stage_data.map_stage.ironGroup, stage_data.myhome)
        stage_data.tanksGroup.add(stage_data.tank_player1)
        stage_data.player1_moving = True
    # Modified, 2022.01.15, 允许在运动的时侯开火
    # elif key_pressed[pygame.K_SPACE]:
    if key_pressed[pygame.K_SPACE]:
        if not stage_data.tank_player1.bullet.being:
            sound_data.fire_sound.play()
            stage_data.tank_player1.shoot()


# 处理玩家二的相关按键事件
# ↑↓←→ -> 上下左右
# 小键盘0键射击
def handle_player2_events(key_pressed, sound_data, stage_data):
    if stage_data.num_player > 1:
        # 用户只要有按住方向键, 则认为tank处于moving状态, 所以设置player2_moving为true
        if key_pressed[pygame.K_UP]:
            stage_data.tanksGroup.remove(stage_data.tank_player2)
            stage_data.tank_player2.move_up(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                            stage_data.map_stage.ironGroup, stage_data.myhome)
            stage_data.tanksGroup.add(stage_data.tank_player2)
            stage_data.player2_moving = True
        elif key_pressed[pygame.K_DOWN]:
            stage_data.tanksGroup.remove(stage_data.tank_player2)
            stage_data.tank_player2.move_down(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                              stage_data.map_stage.ironGroup, stage_data.myhome)
            stage_data.tanksGroup.add(stage_data.tank_player2)
            stage_data.player2_moving = True
        elif key_pressed[pygame.K_LEFT]:
            stage_data.tanksGroup.remove(stage_data.tank_player2)
            stage_data.tank_player2.move_left(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                              stage_data.map_stage.ironGroup, stage_data.myhome)
            stage_data.tanksGroup.add(stage_data.tank_player2)
            stage_data.player2_moving = True
        elif key_pressed[pygame.K_RIGHT]:
            stage_data.tanksGroup.remove(stage_data.tank_player2)
            stage_data.tank_player2.move_right(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
                                               stage_data.map_stage.ironGroup, stage_data.myhome)
            stage_data.tanksGroup.add(stage_data.tank_player2)
            stage_data.player2_moving = True
        # Modified, 2022.01.15, 允许在运动的时侯开火
        # elif key_pressed[pygame.K_KP0]:
        if key_pressed[pygame.K_KP0]:
            if not stage_data.tank_player2.bullet.being:
                sound_data.fire_sound.play()
                stage_data.tank_player2.shoot()


# 用于存放声音相关的数据
class SoundData:
    def __init__(self):
        self.add_sound = pygame.mixer.Sound("./audios/add.wav")
        self.add_sound.set_volume(1)
        self.bang_sound = pygame.mixer.Sound("./audios/bang.wav")
        self.bang_sound.set_volume(1)
        self.blast_sound = pygame.mixer.Sound("./audios/blast.wav")
        self.blast_sound.set_volume(1)
        self.fire_sound = pygame.mixer.Sound("./audios/fire.wav")
        self.fire_sound.set_volume(1)
        self.Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
        self.Gunfire_sound.set_volume(1)
        self.hit_sound = pygame.mixer.Sound("./audios/hit.wav")
        self.hit_sound.set_volume(1)
        self.start_sound = pygame.mixer.Sound("./audios/start.wav")
        self.start_sound.set_volume(1)


# 用于存放每一关对应的数据
class StageData:
    def __init__(self, num_player, stage):
        # 玩家编号, 关卡编号
        self.num_player = num_player
        self.stage = stage
        # 该关卡坦克总数量(敌方库存坦克总量)
        #self.enemytanks_total = min(stage * 18, 80)
        self.enemytanks_total = min(stage * 10, 80)
        # 场上存在的敌方坦克总数量
        self.enemytanks_now = 0
        # 场上可以存在的敌方坦克总数量
        self.enemytanks_now_max = min(max(stage * 2, 4), 8)
        #self.enemytanks_now_max = min(max(stage * 3, 4), 8)
        # 精灵组
        self.tanksGroup = pygame.sprite.Group()
        self.mytanksGroup = pygame.sprite.Group()
        self.enemytanksGroup = pygame.sprite.Group()
        # commented by iron, 2022.01.15
        # bulletsGroup = pygame.sprite.Group()
        # mybulletsGroup = pygame.sprite.Group()
        self.enemybulletsGroup = pygame.sprite.Group()
        # 存放当前随机产生的奖励
        self.myfoodsGroup = pygame.sprite.Group()
        # 自定义事件
        # 	-生成敌方坦克事件
        self.genEnemyEvent = pygame.constants.USEREVENT
        pygame.time.set_timer(self.genEnemyEvent, 100)
        # 	-敌方坦克静止恢复事件
        # self.recoverEnemyEvent = pygame.constants.USEREVENT   # BUG ?
        self.recoverEnemyEvent = pygame.constants.USEREVENT + 1
        #pygame.time.set_timer(self.recoverEnemyEvent, 8000)
        # 	-我方坦克无敌恢复事件
        # self.noprotectMytankEvent = pygame.constants.USEREVENT # BUG ?
        self.noprotectMytankEvent = pygame.constants.USEREVENT + 2
        #pygame.time.set_timer(self.noprotectMytankEvent, 8000)
        # 关卡地图
        self.map_stage = scene.Map(stage)
        # 我方坦克
        self.tank_player1 = tanks.myTank(1)
        # modified,  2022.01.15
        self.tank_player2 = tanks.myTank(2)
        self.tanksGroup.add(self.tank_player1)
        self.mytanksGroup.add(self.tank_player1)
        if num_player > 1:
            # tank_player2 = tanks.myTank(2)
            self.tanksGroup.add(self.tank_player2)
            self.mytanksGroup.add(self.tank_player2)
        # 允许坦克履带特效
        self.is_switch_tank = True
        # 游戏玩家是否按下方向键
        self.player1_moving = False
        self.player2_moving = False
        # 为了轮胎的动画效果
        self.time = 0
        # 敌方坦克
        for i in range(0, 3):
            if self.enemytanks_total > 0:
                enemytank = tanks.enemyTank(i)
                self.tanksGroup.add(enemytank)
                self.enemytanksGroup.add(enemytank)
                self.enemytanks_now += 1
                self.enemytanks_total -= 1
        # 大本营
        self.myhome = home.Home()
        # 用于敌方坦克的出场特效, 由小到大的3颗星星
        appearance_img = pygame.image.load(
            "./images/others/appear.png").convert_alpha()
        self.appearances = []
        self.appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
        self.appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
        self.appearances.append(appearance_img.subsurface((96, 0), (48, 48)))


# 主函数
def main():
    global is_gameover

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((630, 630))
    pygame.display.set_caption("坦克大战")
    # 加载图片
    bg_img = pygame.image.load("./images/others/background.png")
    # 加载音效
    sound_data = SoundData()
    # 开始界面
    num_player = show_start_interface(screen, 630, 630)  # 返回值是1或2，也就获得玩家数
    # 播放游戏开始的音乐, 此函数播放音乐时, 不影响界面刷新
    sound_data.start_sound.play()
    # 关卡
    stage = 0
    #num_stage = NUM_OF_STAGES
    # 游戏是否结束
    is_gameover = False
    # 时钟
    clock = pygame.time.Clock()
    # 主循环
    while not is_gameover:
        # 关卡
        stage += 1
        if stage > NUM_OF_STAGES:
            break
        show_switch_stage(screen, 630, 630, stage)
        stage_data = StageData(num_player, stage)
        # 关卡主循环
        while True:
            if is_gameover:
                break
            # 敌方库存坦克数为0 且战场上坦克也为0
            if stage_data.enemytanks_total < 1 and stage_data.enemytanks_now < 1:
                is_gameover = False
                break
            # 处理不同的事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 结束游戏
                    pygame.quit()
                    sys.exit()
                # 生成新的敌方坦克
                if event.type == stage_data.genEnemyEvent:  # 在 StageData初始化阶段
                    if stage_data.enemytanks_total > 0:  # 材料还够，敌方可以造tank
                        if stage_data.enemytanks_now < stage_data.enemytanks_now_max:  # 场上支持投放敌方tank
                            enemytank = tanks.enemyTank()
                            # 如果 我方坦克 没有 挡住生产处
                            if not pygame.sprite.spritecollide(enemytank, stage_data.tanksGroup, False, None):
                                stage_data.tanksGroup.add(enemytank)
                                stage_data.enemytanksGroup.add(enemytank)
                                stage_data.enemytanks_now += 1
                                stage_data.enemytanks_total -= 1
                # 让被静止的敌方坦克可以移动
                if event.type == stage_data.recoverEnemyEvent:
                    for each in stage_data.enemytanksGroup:
                        each.can_move = True
                # 加在我方坦克上的保护罩到期后失效
                if event.type == stage_data.noprotectMytankEvent:
                    for each in stage_data.mytanksGroup:
                        # BUG
                        #stage_data.mytanksGroup.protected = False
                        each.protected = False
            # 检查用户键盘操作
            key_pressed = pygame.key.get_pressed()

            # 处理玩家一相关键盘事件
            handle_player1_events(key_pressed, sound_data, stage_data)

            # 处理玩家二相关键盘事件
            handle_player2_events(key_pressed, sound_data, stage_data)

            # 重新绘制整个界面:
            # 设置背景图片
            screen.blit(bg_img, (0, 0))
            # 石头墙
            for each in stage_data.map_stage.brickGroup:
                screen.blit(each.brick, each.rect)
            # 钢墙
            for each in stage_data.map_stage.ironGroup:
                screen.blit(each.iron, each.rect)
            # 冰
            for each in stage_data.map_stage.iceGroup:
                screen.blit(each.ice, each.rect)
            # 河流
            for each in stage_data.map_stage.riverGroup:
                screen.blit(each.river, each.rect)
            # 树
            for each in stage_data.map_stage.treeGroup:
                screen.blit(each.tree, each.rect)
            # 5个滴答里, 允许is_switch_tank翻转一次
            stage_data.time += 1
            if stage_data.time == 5:
                stage_data.time = 0
                stage_data.is_switch_tank = not stage_data.is_switch_tank
            # 我方坦克
            handle_mytanksGroup(stage_data, screen)
            # 敌方坦克
            handle_enemytanksGroup(stage_data, screen)
            # 我方子弹
            handle_mybullet(stage_data, sound_data, screen)
            # 敌方子弹
            handle_enemy_bullet(stage_data, sound_data, screen)
            # 家
            screen.blit(stage_data.myhome.home, stage_data.myhome.rect)
            # 食物
            handle_food(stage_data, sound_data, screen)

            # 窗口标题
            if stage_data.num_player == 1:
                pygame.display.set_caption("坦克大战: 第{0}关, 我方库存坦克数 {1}, 敌方库存坦克数 {2}".format(
                    stage_data.stage,
                    stage_data.tank_player1.life,
                    stage_data.enemytanks_total))
            else:
                pygame.display.set_caption("坦克大战: 第{0}关, 我方库存坦克数 ({1},{2}), 敌方库存坦克数 {3}".format(
                    stage_data.stage,
                    stage_data.tank_player1.life, stage_data.tank_player2.life,
                    stage_data.enemytanks_total))
            pygame.display.flip()
            clock.tick(60)
    if not is_gameover:
        show_end_interface(screen, 630, 630, True)  # 赢了
    else:
        show_end_interface(screen, 630, 630, False)


if __name__ == '__main__':
    main()
