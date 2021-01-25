#Attribute Stephen "Redshrike" Challener as graphic artist and William.Thompsonj as contributor.
#Created by Svetlana Kushnariova (Cabbit) <lana-chan@yandex.ru>, Stephen Challener (Redshrike), One Man Army, DkuCook, & Jordan Irwin (AntumDeluge)
#Stephen Challener (Redshrike), hosted by OpenGameArt.org
#Credit would be nice: 'NicoleMarieProductions'
import pygame as pg
import random
from os import path
import math
import time
import cv2


FPS = 60
TITLE = 'Raycasting par Dean Zhang'
TILE_SIZE = 80
MAP_NUM_ROWS = 9
MAP_NUM_COLS = 16
WIDTH = MAP_NUM_COLS * TILE_SIZE #1280
HEIGHT = MAP_NUM_ROWS * TILE_SIZE #720
FOV_ANGLE = 60 * math.pi / 180
WALL_STRIP_WIDTH = 1
NUM_RAYS = int(WIDTH / WALL_STRIP_WIDTH)
MINI_MAP_SCALE_FACTOR = 0.2
img_folder = path.join(path.dirname(__file__), 'Img')
snd_folder = path.join(path.dirname(__file__), 'Snd')
texts_folder = path.join(img_folder, 'Textures')
font_name = pg.font.match_font('arial')
randomness_player = 0.1
randomness_ennemy = 0.1



#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (105,105,105)

pg.init()
pg.mixer.init()
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

##############################################33
###################TEST PLAYER SPEEED AND ROTATION SPEED
#############################################
class Map:
	def __init__(self):
		self.grid = [
	[1,1,1,1,1,1,2,1,2,1,1,3,1,1,1,1],
	[1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,2],
	[1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,4],
	[1,0,1,1,3,0,0,0,1,0,0,3,0,0,0,1],
	[1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,2],
	[1,3,2,0,1,0,1,0,0,1,0,2,0,0,0,1],
	[1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,2],
	[1,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1],
	[1,1,1,1,1,1,1,1,1,1,3,1,2,1,4,1]
	]

	def hasWallAt(self, x, y):
		if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
			return True
		mapGridIndexX = int(x / TILE_SIZE)
		mapGridIndexY = int(y / TILE_SIZE)
		return self.grid[mapGridIndexY][mapGridIndexX]
	

	def draw(self, win):
		for i in range(0,MAP_NUM_ROWS):
			for j in range(0,MAP_NUM_COLS):
				pg.draw.line(win, BLACK, (MINI_MAP_SCALE_FACTOR * j * TILE_SIZE, MINI_MAP_SCALE_FACTOR * 0), (MINI_MAP_SCALE_FACTOR * j * TILE_SIZE, MINI_MAP_SCALE_FACTOR * HEIGHT))
				pg.draw.line(win, BLACK, (MINI_MAP_SCALE_FACTOR * 0, MINI_MAP_SCALE_FACTOR * i*TILE_SIZE), (MINI_MAP_SCALE_FACTOR * WIDTH, MINI_MAP_SCALE_FACTOR * i * TILE_SIZE))

				tileX = j * TILE_SIZE
				tileY = i * TILE_SIZE
				tileColor = WHITE
				if self.grid[i][j] != 0:
					tileColor = BLACK
				pg.draw.rect(win, tileColor, pg.Rect(
				MINI_MAP_SCALE_FACTOR * tileX,
				MINI_MAP_SCALE_FACTOR * tileY, 
				MINI_MAP_SCALE_FACTOR * TILE_SIZE, 
				MINI_MAP_SCALE_FACTOR * TILE_SIZE ))

class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.x = 90
		self.y = HEIGHT / 2
		wideness = 15
		self.rect = pg.Rect(0,0,wideness,wideness)
		self.radius = wideness
		self.rect.center = self.x, self.y
		self.turnDirection = 0      #-1 if left, 1 if right
		self.walkDirection = 0      #-1 if back, 1 if front
		self.walkDirectionLR = 0    #-1 left, 1 right
		self.rotationAngle = math.pi / 2 * 3
		self.moveSpeed = 10.0
		self.rotationSpeed = 7 * (math.pi / 180)
		self.shoot_delay = 250
		self.last_shot = pg.time.get_ticks()
		self.hp = 100
		self.lives = 3
		self.ms_sensitivity = math.pi / 180 *  0.12

	def keyPressed(self):
		keystate = pg.key.get_pressed()
		if keystate[pg.K_w] and keystate[pg.K_s]:
			self.walkDirection = 0
		elif keystate[pg.K_w]:
			self.walkDirection = 1
		elif keystate[pg.K_s]:
			self.walkDirection = -1
		else:
			self.walkDirection = 0

		if keystate[pg.K_a] and keystate[pg.K_d]:
			self.walkDirectionLR = 0
		elif keystate[pg.K_d]:
			self.walkDirectionLR = 1
		elif keystate[pg.K_a]:
			self.walkDirectionLR = -1
		else:
			self.walkDirectionLR = 0

		if keystate[pg.K_LEFT] and keystate[pg.K_RIGHT]:
			self.turnDirection = 0
		elif keystate[pg.K_RIGHT]:
			self.turnDirection = 1
		elif keystate[pg.K_LEFT]:
			self.turnDirection = -1
		else:
			self.turnDirection = 0

		mousestate = pg.mouse.get_pressed(num_buttons=3)
		if keystate[pg.K_SPACE] or mousestate[0]:
			self.shoot()

	def shoot(self):
		global bullet_sprites
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			shoot_snd.play()
			bullet = Bullet(grid, self.x, self.y, HEIGHT / 100, path.join(path.join(img_folder, 'Bullet'), 'Bullet.png'),BLUE, self.rotationAngle, 50, bullet_text, True, randomness_player)
			bullet_sprites.add(bullet)


	def update(self, grid):
		self.keyPressed()
		self.rotationAngle += self.turnDirection * self.rotationSpeed
		difX = pg.mouse.get_rel()[0]
		self.rotationAngle += difX * self.ms_sensitivity
		self.rotationAngle = normaliseAngle(self.rotationAngle)
		ang_rot = self.rotationAngle
		if self.walkDirectionLR == 1:
			ang_rot += (math.pi / 2)	
			if self.walkDirection == 1:
				ang_rot -= (math.pi / 4)	
			elif self.walkDirection == -1:
				ang_rot += (math.pi * 1 / 4)
		elif self.walkDirectionLR == -1:
			ang_rot -= (math.pi / 2)
			if self.walkDirection == 1:
				ang_rot += (math.pi / 4)	
			elif self.walkDirection == -1:
				ang_rot -= (math.pi * 1 / 4)

		elif self.walkDirectionLR == 0:
			if self.walkDirection == 1:
				ang_rot = self.rotationAngle
			elif self.walkDirection == -1:
				ang_rot = self.rotationAngle - math.pi		

		moveStep = self.walkDirection * self.moveSpeed

		if self.walkDirectionLR != 0 or self.walkDirection != 0:
			newPosX = self.x + math.cos(ang_rot) * self.moveSpeed
			newPosY = self.y + math.sin(ang_rot)* self.moveSpeed

			#set new position if there is no wall
			if not grid.hasWallAt(newPosX, newPosY):
				self.x = newPosX
				self.y = newPosY
				self.rect.center = self.x, self.y

	def draw(self, win):
		pg.draw.circle(win, RED, (int(MINI_MAP_SCALE_FACTOR * self.x), int(MINI_MAP_SCALE_FACTOR * self.y)), int(MINI_MAP_SCALE_FACTOR * self.radius))
		#pg.draw.line(win, RED, (int(self.x), int(self.y)), (self.x + math.cos(self.rotationAngle) * 20, self.y + math.sin(self.rotationAngle) * 20))

class Ray:
	def __init__(self, rayAngle):
		self.rayAngle = normaliseAngle(rayAngle)
		self.wallHitX = 0
		self.wallHitY = 0
		self.distance = 0
		self.isRayFacingDown = self.rayAngle > 0 and self.rayAngle < math.pi
		self.isRayFacingUp = not self.isRayFacingDown
		self.isRayFacingRight = self.rayAngle < 0.5 * math.pi or self.rayAngle > 1.5 * math.pi 
		self.isRayFacingLeft = not self.isRayFacingRight
		self.wasHitVert = False
		self.wallHit = None

	def cast(self, player, grid):
		############
		#HORIZONTAL
		############
		foundHorzWallHit = False
		horzWallHitX = 0
		horzWallHitY = 0
		yintercept = int(player.y / TILE_SIZE) * TILE_SIZE
		if self.isRayFacingDown:
			yintercept += TILE_SIZE
		xintercept = player.x + (yintercept - player.y) / math.tan(self.rayAngle)

		#Xstep and Ystep
		ystep = TILE_SIZE
		if self.isRayFacingUp:
			ystep *= -1
		xstep = TILE_SIZE / math.tan(self.rayAngle)
		if self.isRayFacingLeft and xstep > 0 or self.isRayFacingRight and xstep < 0:
			xstep *= -1

		nextHorzTouchX = xintercept
		nextHorzTouchY = yintercept


		while nextHorzTouchX >= 0 and nextHorzTouchX <= WIDTH and nextHorzTouchY >= 0 and nextHorzTouchY <= HEIGHT:
			if self.rayAngle == 0 or self.rayAngle == math.pi:
				break
			temp = nextHorzTouchY
			if self.isRayFacingUp:
				temp -= 1
			if grid.hasWallAt(nextHorzTouchX, temp):
				horzWallHit = grid.hasWallAt(nextHorzTouchX, temp)
				foundHorzWallHit = True
				horzWallHitX = nextHorzTouchX
				horzWallHitY = nextHorzTouchY
				break
			else:
				nextHorzTouchX += xstep
				nextHorzTouchY += ystep
		############
		#VERTICAL	
		############
		foundVertWallHit = False
		VertwallHitX = 0
		VertwallHitY = 0
		xintercept = int(player.x / TILE_SIZE) * TILE_SIZE
		if self.isRayFacingRight:
			xintercept += TILE_SIZE
		yintercept = player.y + (xintercept - player.x) * math.tan(self.rayAngle)

		#Xstep and Ystep
		xstep = TILE_SIZE
		if self.isRayFacingLeft:
			xstep *= -1
		ystep = TILE_SIZE * math.tan(self.rayAngle)
		if self.isRayFacingUp and ystep > 0 or self.isRayFacingDown and ystep < 0:
			ystep *= -1

		nextVertTouchX = xintercept
		nextVertTouchY = yintercept

		while nextVertTouchX >= 0 and nextVertTouchX <= WIDTH and nextVertTouchY >= 0 and nextVertTouchY <= HEIGHT:
			if self.rayAngle == math.pi / 2 or self.rayAngle == math.pi * 3/4:
				break
			temp = nextVertTouchX
			if self.isRayFacingLeft:
				temp -= 1
			if grid.hasWallAt(temp, nextVertTouchY):
				vertWallHit = grid.hasWallAt(temp, nextVertTouchY)
				foundVertWallHit = True
				vertWallHitX = nextVertTouchX
				vertWallHitY = nextVertTouchY
				break
			else:
				nextVertTouchX += xstep
				nextVertTouchY += ystep

		###################################
		###Calculate the lowest distance
		##################################
		horzWallDist = float('inf')
		if foundHorzWallHit:
			horzWallDist = distanceBetweenPoints(player.x, player.y, horzWallHitX, horzWallHitY)
		vertWallDist = float('inf')
		if foundVertWallHit:
			vertWallDist = distanceBetweenPoints(player.x, player.y, vertWallHitX, vertWallHitY)

		if vertWallDist < horzWallDist:
			self.wallHit = vertWallHit
			self.wallHitX = vertWallHitX
			self.wallHitY = vertWallHitY
			self.distance = vertWallDist
			self.wasHitVert = True
		else:
			self.wallHit = horzWallHit
			self.wallHitX = horzWallHitX
			self.wallHitY = horzWallHitY
			self.distance = horzWallDist
			self.wasHitVert = False

	def draw(self,win, player):
		pg.draw.line(win, BLUE, (int(MINI_MAP_SCALE_FACTOR * player.x), int(MINI_MAP_SCALE_FACTOR * player.y)),(int(MINI_MAP_SCALE_FACTOR * self.wallHitX), int(MINI_MAP_SCALE_FACTOR * self.wallHitY)))

class Object(pg.sprite.Sprite):
	def __init__(self, grid, x, y, height, imgpath, color, array):
		global all_sprites
		pg.sprite.Sprite.__init__(self)
		all_sprites.add(self)
		if grid.hasWallAt(x, y):
			self.kill()
		self.x = x
		self.y = y
		img = cv2.imread(imgpath)
		self.row, self.col, a = img.shape
		self.height = height
		self.color = color
		self.array = array
		width = self.col * self.height / self.row
		self.rect = pg.Rect(0,0,width,width)
		self.rect.center = self.x, self.y


	def is_drawable(self, player):
		self.distToObj = distanceBetweenPoints(self.x, self.y, player.x, player.y)
		VecX = self.x - player.x;
		VecY = self.y - player.y;
		player.rotationAngle = normaliseAngle(player.rotationAngle)
		if VecX == 0 and VecY > 0:
			objThetaToPlane = math.pi / 2
		elif VecX == 0 and VecY < 0:
			objThetaToPlane = 3 / 2 * math.pi
		elif VecX < 0 and VecY == 0:
			objThetaToPlane = math.pi
		elif VecX > 0 and VecY == 0 or VecX == 0 and VecY == 0:
			objThetaToPlane = 0
		else:
			objThetaToPlane = math.atan(VecY / VecX)
		if (VecX < 0 and VecY > 0) or (VecX < 0 and VecY < 0):
			objThetaToPlane += math.pi
		elif VecX > 0 and VecY < 0:
			objThetaToPlane += (2 * math.pi)
		self.objThetaToPlane = objThetaToPlane
		self.objTheta = abs(player.rotationAngle - objThetaToPlane)

		self.is_left = True
		if player.rotationAngle - objThetaToPlane > 0:
			self.is_left = False

		if VecX > 0 and VecY < 0 and player.rotationAngle >= 0 and player.rotationAngle <= math.pi / 2:
			self.objTheta = 2 * math.pi - objThetaToPlane + player.rotationAngle
			self.is_left = False
		elif VecX > 0 and VecY > 0 and player.rotationAngle >= 3 / 2 * math.pi and player.rotationAngle <= 2 * math.pi:
			self.objTheta = 2 * math.pi - player.rotationAngle + objThetaToPlane
			self.is_left = True

		if not isinstance(self, Bullet):
			pg.draw.rect(win, self.color, pg.Rect(self.rect.centerx * MINI_MAP_SCALE_FACTOR, self.rect.centery * MINI_MAP_SCALE_FACTOR, self.rect.width* MINI_MAP_SCALE_FACTOR, self.rect.height* MINI_MAP_SCALE_FACTOR))

		if isinstance(self, Bullet):
			min_dist = self.distToObj >= 20
		else:
			min_dist = self.distToObj >= self.rect.width
		if self.objTheta <= FOV_ANGLE / 2 and min_dist:
			return True
		return False

	def draw(self, win, player):

		#heigh of the wall
		try:
			correctWallDistance = self.distToObj * math.cos(self.objTheta)
			distanceProjectionPlane = (WIDTH / 2) / (math.tan(FOV_ANGLE / 2))
			wallStripHeight = TILE_SIZE / correctWallDistance * distanceProjectionPlane

			#height of the object]
			real_height = self.height * wallStripHeight / TILE_SIZE
			real_width = self.col * real_height / self.row
			yPosFloor = (HEIGHT / 2) + (wallStripHeight / 2)
			ypos = yPosFloor - real_height
			thetatoleftside = self.objTheta + FOV_ANGLE / 2
			if not self.is_left:
				thetatoleftside = FOV_ANGLE / 2 - self.objTheta
			if isinstance(self, Bullet):
				ypos = HEIGHT / 2 - real_height/2
		except:
			return
		for i in range(self.col):
			try:
				xpos = (thetatoleftside * WIDTH / FOV_ANGLE) - real_width / 2 + i * real_width / self.col
				if xpos > WIDTH:
					xpos = WIDTH
				if xpos < 0:
					xpos = 0
				ray_distance = list_dist_rays[math.floor((len(list_dist_rays) - 1) * xpos / WIDTH)]
				if ray_distance > self.distToObj:	
					objectimg = pg.transform.scale(self.array[i],(int(real_width / self.col) + 1,int(real_height)))
					if isinstance(self, Ennemy):
						objectimg.set_colorkey(RED)
					else:
						objectimg.set_colorkey(BLACK)
					win.blit(objectimg, (xpos, ypos))
			except:
				continue

class Bullet(Object):
	def __init__(self, grid, x, y, height, imgpath, color, theta, speed, array, isfriendlybullet, randomness):
		super().__init__(grid, x, y, height, imgpath, color, array)
		self.theta = normaliseAngle(theta)
		self.speed = speed
		self.isfriendlybullet = isfriendlybullet
		random_num = random.choice([-1, 1]) * random.uniform(0, randomness)
		self.vx = math.cos(self.theta + random_num) * speed
		self.vy = math.sin(self.theta + random_num)* speed
 
	def update(self, grid, ):
		global bullet_sprites, all_sprites, list_ennemy_bullet
		newPosX = self.x + self.vx
		newPosY = self.y + self.vy

		#set new position if there is no wall
		if grid.hasWallAt(newPosX, newPosY):
			self.kill()
		self.x = newPosX
		self.y = newPosY
		self.rect.center = self.x, self.y

class Ennemy(Object):
	def __init__(self, grid, x, y, height, imgpath, color, array):
		super().__init__(grid, x, y, height, imgpath, color, array)
		self.shoot_delay = 1000
		self.last_shot = pg.time.get_ticks()
		self.hp = 50

	def can_see_player(self, player):
		self.is_drawable(player)
		ray = Ray(self.objThetaToPlane + math.pi)
		ray.cast(self, grid)
		if self.distToObj <= ray.distance:
			return True
		return False

	def update(self, player):
		global list_pow
		if self.hp <= 0:
			if random.random() > 0:
				power = Pow(self.x, self.y)
				all_sprites.add(power)
				list_pow.add(power)
			self.kill()
		if self.can_see_player(player):
			self.shoot()


	def shoot(self):
		global list_ennemy_bullet
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			ennemy_shoot_snd.play()
			left = self.objThetaToPlane + math.pi / 2
			if random.random() > 0.5:
				left = self.objThetaToPlane - math.pi / 2
			correctWallDistance = self.distToObj * math.cos(self.objTheta)
			distanceProjectionPlane = (WIDTH / 2) / (math.tan(FOV_ANGLE / 2))
			wallStripHeight = TILE_SIZE / correctWallDistance * distanceProjectionPlane

			#height of the object]
			real_height = self.height * wallStripHeight / TILE_SIZE
			real_width = self.col * real_height / self.row
			dist = 1/10 * real_width
			bullet = Bullet(grid, self.x + math.cos(left) * dist, self.y + math.sin(left) * dist, HEIGHT / 100, path.join(path.join(img_folder, 'EnnemyBullet'), 'EnnemyBullet.png'),BLUE, self.objThetaToPlane + math.pi, 20, ennemy_bullet_text, False, randomness_ennemy)
			list_ennemy_bullet.add(bullet)

class Pow(Object):
	def __init__(self, x, y):
		global grid
		powers = {
		'pill_red': (20, path.join(path.join(img_folder, 'Pill_red'), 'Pill_red.png'), RED, pill_red_text),  
		'pill_blue': (20, path.join(path.join(img_folder, 'Pill_blue'), 'Pill_blue.png'), BLUE,pill_blue_text),
		'crossair' : (20, path.join(path.join(img_folder, 'Crossair'), 'Crossair.png'), BLACK, crossair_text)
		}
		self.type = random.choice(['pill_red', 'pill_blue','pill_red','pill_red' , 'crossair', 'crossair', 'crossair'])
		super().__init__(grid, x, y, powers[self.type][0], powers[self.type][1], powers[self.type][2], powers[self.type][3])


def draw3DProjectedWalls(win, player):
	global list_dist_rays
	list_dist_rays = []
	for i in range(0, NUM_RAYS):
		ray = rays[i]
		correctWallDistance = ray.distance * math.cos(ray.rayAngle - player.rotationAngle)
		distanceProjectionPlane = (WIDTH / 2) / (math.tan(FOV_ANGLE / 2))
		wallStripHeight = TILE_SIZE / correctWallDistance * distanceProjectionPlane
	
		list_dist_rays.append(ray.distance)

		text = WALL_TEXT_DICT[ray.wallHit]
		if ray.wasHitVert:
			distToleft = TILE_SIZE - (ray.wallHitY % TILE_SIZE)
		else:
			distToleft = ray.wallHitX % TILE_SIZE


		column = text[int(distToleft * len(text) / TILE_SIZE)]
		if wallStripHeight - HEIGHT > 0:
			gap = (wallStripHeight - HEIGHT) /2 / wallStripHeight * column.get_height()
			real_height = column.get_height() - 2 * (math.floor(gap))
			temp = pg.Surface((WALL_STRIP_WIDTH, real_height))
			temp.blit(column, (0,0), (0, math.floor(gap), WALL_STRIP_WIDTH, real_height))
			wallStripHeight = real_height / column.get_height() * wallStripHeight
			column = pg.transform.scale(temp,(int(WALL_STRIP_WIDTH),int(wallStripHeight)))
		else:
			column = pg.transform.scale(column,(int(WALL_STRIP_WIDTH),int(wallStripHeight)))
		#	if textBlockHeight > HEIGHT:
		#		textBlockHeight = HEIGHT
		ypos = (HEIGHT / 2) - (wallStripHeight / 2)
		win.blit(column, (i, ypos))

def distanceBetweenPoints(x1, y1, x2, y2):
	return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def normaliseAngle(angle):
	angle = angle % (math.pi * 2)
	if angle < 0:
		angle += (2 * math.pi)

	return angle

def castAllRays(player, grid, win):
	global rays
	rayAngle = player.rotationAngle - (FOV_ANGLE / 2)   # first ray
	rays = []
	for i in range(0, NUM_RAYS):
	#for i in range(0, 1):
		ray = Ray(rayAngle)
		ray.cast(player, grid)
		rays.append(ray)
		rayAngle += FOV_ANGLE / NUM_RAYS

def show_go_screen():
	pg.event.set_grab(False)
	pg.mouse.set_visible(True)
	win.fill(BLUE)
	win.blit(background, background_rect)
	draw_text(win, 'RAYCASTING!', 54, WIDTH / 2, HEIGHT / 4, BLACK)
	draw_text(win, 'WASD pour bouger. Espace et la souris pour tirer', 22, WIDTH / 2, HEIGHT / 2, BLACK)
	draw_text(win, 'Touches directionnelles et la caméra pour tourner la caméra', 22, WIDTH / 2, HEIGHT / 2 + 40, BLACK)
	draw_text(win, 'Échappe pour arrêter le jeu', 22, WIDTH / 2, HEIGHT / 2 + 40 + 40, BLACK)
	draw_text(win, 'Peser une touche pour commencer', 18, WIDTH / 2, HEIGHT * 3/4, BLACK)
	pg.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

def win_screen():
	global music_on
	draw_text(win, 'TU AS GAGNÉ!!!',  100,  WIDTH//2, HEIGHT//2,BLACK)
	draw_text(win,'Peser une touche pour continuer', 25, WIDTH//2, HEIGHT//2 + 100, BLACK)
	pg.display.flip()
	music_on = False
	pg.mixer.music.stop()
	pg.mixer.music.load(path.join(snd_folder, 'Victory.ogg'))
	pg.mixer.music.set_volume(0.9)
	pg.mixer.music.play(loops=-1)
	time.sleep(4)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				waiting = False
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

def lost_screen():
	draw_text(win, 'Tu as perdu...',  100,  WIDTH//2, HEIGHT//2,BLACK)
	draw_text(win,'Peser une touche pour continuer', 25, WIDTH//2, HEIGHT//2 + 100, BLACK)
	pg.display.flip()
	time.sleep(4)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				waiting = False
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

def draw_shield_bar(surf, x,y,pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGTH = 10
	fill = (pct/100) * BAR_LENGTH
	outline_rect = pg.Rect(x,y,BAR_LENGTH, BAR_HEIGTH)
	fill_rect = pg.Rect(x,y,fill,BAR_HEIGTH)
	pg.draw.rect(surf, GREEN, fill_rect)
	pg.draw.rect(surf, WHITE, outline_rect,2) #2=

def update():
	global game_over, randomness_player
	player.update(grid)
	castAllRays(player, grid, win)
	bullet_sprites.update(grid)

	list_ennemy.update(player)

	list_ennemy_bullet.update(grid)

	hits = pg.sprite.groupcollide(list_ennemy, bullet_sprites, False, True)
	for hit in hits:
		hit.hp -= 10
		bow_snd.play()

	hits = pg.sprite.groupcollide(list_objects, bullet_sprites, False, True)
	for hit in hits:
		metal_snd.play()
	hits = pg.sprite.groupcollide(list_objects, list_ennemy_bullet, False, True)
	for hit in hits:
		metal_snd.play()
	hits = pg.sprite.spritecollide(player, list_ennemy, True)
	for hit in hits:
		player.hp -= 50
		pain2_snd.play()


	hits = pg.sprite.spritecollide(player, list_ennemy_bullet, True)
	for hit in hits:
		player.hp -= 20
		pain1_snd.play()

	if player.hp <= 0:
		Almost_death_snd.play()
		player.lives -= 1
		player.hp = 100

	hits = pg.sprite.spritecollide(player, list_pow, True)
	for hit in hits:
		power_snd.play()
		if hit.type == 'pill_red':
			player.hp += random.randrange(10,31)
			if player.hp >= 100:
				player.hp = 100		
		if hit.type == 'pill_blue':
			player.lives += 1
			if player.lives > 4:
				player.lives = 4	
		if hit.type == 'crossair':
			randomness_player -= 0.05
			if randomness_player < 0:
				randomness_player = 0

	if player.lives <= 0:
		death_snd.play()
		lost_screen()
		game_over = True

	if len(list_ennemy.sprites()) <= 0:
		win_screen()
		game_over = True

def draw_text(surf,text,size, x, y, color):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface, text_rect)

def draw_lives(surf, x,y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img, img_rect)

def draw():
	win.fill(GREY)
	draw3DProjectedWalls(win, player)
	grid.draw(win)
	for ray in rays:
		ray.draw(win, player)
	player.draw(win)
	drawable_objects = {}

	for obj in all_sprites:
		if obj.is_drawable(player):
			drawable_objects[obj] = obj.distToObj

	drawable_objects = sorted(drawable_objects.items(), key=lambda x:x[1], reverse=True)
	for obj in drawable_objects:
		obj[0].draw(win, player)

		#cross air
	pg.draw.line(win, WHITE, ( WIDTH / 2, HEIGHT / 2 - 10), ( WIDTH / 2, HEIGHT / 2 + 10))
	pg.draw.line(win, WHITE, (WIDTH / 2 - 10, HEIGHT / 2),(WIDTH / 2 + 10, HEIGHT / 2)) 
	draw_shield_bar(win, 5,5,player.hp)
	draw_lives(win, WIDTH - 100, 5, player.lives, heart)


def load_text(num):
	text_folder = path.join(texts_folder,  f'texture{num}')
	list_text = []
	img = cv2.imread(path.join(text_folder, f'walls.png'))
	row, cols, a = img.shape
	for col in range(cols):
		col_pix = img[0:row+1, col:col+1]
		cv2.imwrite(path.join(text_folder, f'wall{col}.png') ,col_pix)
		list_text.append(pg.image.load(path.join(text_folder, f'wall{col}.png')).convert())
	return list_text

def load(name):
	obj_folder = path.join(path.join(img_folder,  name), f'{name}.png')
	list_obj = []
	img = cv2.imread(path.join(path.join(img_folder,  name), f'{name}.png'))
	row, cols, a = img.shape
	for col in range(cols):
		col_pix = img[0:row+1, col:col+1]
		cv2.imwrite(path.join(path.join(img_folder,  name), f'{name}{col}.png') ,col_pix)
		list_obj.append(pg.image.load(path.join(path.join(img_folder,  name), f'{name}{col}.png')).convert())
	return list_obj


def pause(win):
	draw_text(win, 'PAUSE', 80, WIDTH / 2, HEIGHT / 2, RED)
	draw_text(win, 'Échappe pour continuer', 22, WIDTH / 2, HEIGHT /2 + 80, BLACK)
	pg.event.set_grab(False)
	pg.mouse.set_visible(True)
	pg.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					waiting = False
					pg.event.set_grab(True)
					pg.mouse.set_visible(False)


#############################
#
#       INITIALIZATION
#
###########################

#####Graphics 
texture = load_text(1)
texture2 = load_text(2)
WALL_TEXT_DICT = {1:texture, 2:texture2, 3:texture, 4:texture2}

bullet_text = load('Bullet')
lamp_text = load('Lamp')
ennemy_text = load('Ennemi')
ennemy_bullet_text = load('EnnemyBullet')
pill_red_text = load('Pill_red')
pill_blue_text = load('Pill_blue')
crossair_text = load('Crossair')


background = pg.image.load(path.join(img_folder, 'Background.png')).convert()
background = pg.transform.scale(background,(WIDTH, HEIGHT))
background_rect = background.get_rect()
heart = pg.image.load(path.join(img_folder, 'Heart.png')).convert()
heart.set_colorkey(BLACK)

####Sounds
shoot_snd = pg.mixer.Sound(path.join(snd_folder, 'Shoot.wav'))
shoot_snd.set_volume(0.3)
ennemy_shoot_snd = pg.mixer.Sound(path.join(snd_folder, 'Ennemy_shoot.wav'))
ennemy_shoot_snd.set_volume(0.2)
Almost_death_snd = pg.mixer.Sound(path.join(snd_folder, 'Almost_death.ogg'))
metal_snd = pg.mixer.Sound(path.join(snd_folder, 'Metal.wav'))
metal_snd.set_volume(0.6)
pain1_snd = pg.mixer.Sound(path.join(snd_folder, 'Grunt.wav'))
pain2_snd = pg.mixer.Sound(path.join(snd_folder, 'Pain.wav'))
death_snd = pg.mixer.Sound(path.join(snd_folder, 'Death.wav'))
bow_snd = pg.mixer.Sound(path.join(snd_folder, 'Bow.wav'))
bow_snd.set_volume(1.2)
power_snd = pg.mixer.Sound(path.join(snd_folder, 'Powerup.wav'))
power_snd.set_volume(0.5)


pg.mixer.music.load(path.join(snd_folder, 'Bkg_music.ogg'))
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(loops=-1)


###################################
#
#      LOOP
#
###########################
music_on = True
running = True
game_over = True
while running:
	if game_over:
		show_go_screen()
		game_over = False
		grid = Map()
		player = Player()
		rays = []

		bullet_sprites = pg.sprite.Group()
		all_sprites = pg.sprite.Group()
		list_objects = pg.sprite.Group()
		drawable_objects = []
		list_ennemy = pg.sprite.Group()
		list_ennemy_bullet = pg.sprite.Group()
		list_pow = pg.sprite.Group()


		lamp = Object(grid, WIDTH/2 + 1,HEIGHT/2 + 1, 40, path.join(path.join(img_folder, 'Lamp'), 'Lamp.png'), GREEN, lamp_text)
		lamp2 = Object(grid, WIDTH/2 + 50,HEIGHT/2 + 50, 40, path.join(path.join(img_folder, 'Lamp'), 'Lamp.png'), GREEN, lamp_text)
		list_objects.add(lamp)
		list_objects.add(lamp2)

		for i in range(10):
			ennemy = Ennemy(grid, random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 90, path.join(path.join(img_folder, 'Ennemi'), 'Ennemi.png'), GREY, ennemy_text)
			list_ennemy.add(ennemy)
			if grid.hasWallAt(ennemy.x, ennemy.y):
				ennemy.kill()
		ennemy1 = Ennemy(grid, WIDTH/2 + 100,HEIGHT/2 + 100, 100, path.join(path.join(img_folder, 'Ennemi'), 'Ennemi.png'), GREY, ennemy_text)
		list_ennemy.add(ennemy1)

		score = 0

		if not music_on:
			pg.mixer.music.stop()
			pg.mixer.music.load(path.join(snd_folder, 'Bkg_music.ogg'))
			pg.mixer.music.set_volume(0.4)
			pg.mixer.music.play(loops=-1)
			music_on = True
		pg.event.set_grab(True)
		pg.mouse.set_visible(False)

	#running at right speed
	clock.tick(FPS)
	#process input(event)
	for event in pg.event.get():	
		if event.type == pg.QUIT:
			running = False 
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				pause(win)
	#update
	update()

	#draw/render
	draw()

	#after drawing everything
	pg.display.flip()

pg.quit()