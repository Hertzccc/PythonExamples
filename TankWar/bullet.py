# coding: utf-8
# 子弹类
import pygame


# 子弹类
class Bullet(pygame.sprite.Sprite):  # 12 * 12 小精灵类
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 子弹四个方向(上下左右) 载入图片
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# 子弹方向(默认向上) x在横轴右为正向，y为纵轴下为正向
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		# 在坦克类中再赋实际值
		self.rect.left, self.rect.right = 0, 0
		# 速度
		self.speed = 6
		# 是否存活
		self.being = False
		# 是否为加强版子弹(可碎钢板)
		self.stronger = False

	# 改变子弹方向
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		# 根据不同的朝向, 加载不同的子弹外观，对应方向根据xy
		if self.direction_x == 0 and self.direction_y == -1:    # UP
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:   # DOWN
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:  # LEFT
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:   # RIGHT
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')

	# 移动
	# 针对子弹，速度乘x方向， 和速度乘y方向；
	def move(self): 
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		# 到地图边缘后消失， 因为地图旁边预留3像素，左和上 < 3, 右和上 > 627
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3):
			self.being = False
