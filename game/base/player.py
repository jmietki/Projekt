# -*- coding: utf-8 -*-

import pyglet 
from pyglet.window import key

import physicalobject

# Flagi dla określenia w którą strone jest skierowany
LEFT  = 0x01
RIGHT = 0x02
STOP  = 0x04
IN_AIR = 0x08
ON_GROUND = 0x16

class MuzzleEffect(pyglet.sprite.Sprite):
	"""docstring for MuzzleEffect"""
	def __init__(self, *args, **kwargs):
		super(MuzzleEffect, self).__init__(*args, **kwargs)

		self.visible = False
		self.visible_time = 0
		self.visible_time_default = 0.4
		self.offset_x = 150
		self.offset_y = 100

	def update(self, dt, x, y):
		self.visible_time += dt
		if self.visible_time >= self.visible_time_default:
			self.visible_time = 0
			self.visible = False
		self.x = x + self.offset_x
		self.y = y + self.offset_y
		self.opacity -= 40*self.visible_time

	def show(self, x, y):
		self.visible = True
		self.x = x + self.offset_x
		self.y = y + self.offset_y
		self.opacity = 255

class Player(physicalobject.PhysicalObject):
	""" Główna klasa gracza Player"""

	def __init__(self, resources):
		super(Player, self).__init__(resources.images['player_stand_right'])

		# dostęp do zasobów
		self.game_resources = resources

		# Domyślne flagi
		self.facing  = RIGHT
		self.status  = ON_GROUND
		self.walking = STOP 

		# Domyślne wartości prędkości i siły skoku
		self.default_speed = 350
		self.default_jump = 850

		# Lista obiektów kolizyjnych
		self.collision_objects = None

		self.scale = 0.7

		# muzzle effect
		self.muzzle_right = MuzzleEffect(resources.images['muzzle_right'])
		self.muzzle_right.scale = self.scale

		self.muzzle_left = MuzzleEffect(resources.images['muzzle_left'])
		self.muzzle_left.offset_x = -70
		self.muzzle_left.scale = self.scale

	def move_right(self):
	 	self.velocity_x = self.default_speed
	 	self.facing  = RIGHT
	 	self.walking = RIGHT
	 	self.set_image()

	def move_left(self):
	 	self.velocity_x = -self.default_speed
	 	self.facing = LEFT
	 	self.walking = LEFT
		self.set_image()

	def jump(self):
		if self.status == ON_GROUND:
			self.velocity_y = self.default_jump
			self.status = IN_AIR
			self.set_image()

	def land(self):
		self.status = ON_GROUND
		self.set_image()

	def stop(self):
		self.velocity_x = 0
		self.walking = STOP
		self.set_image()

	def fire(self):
		if self.facing == LEFT:
			self.muzzle_left.show(self.x, self.y)
		if self.facing == RIGHT:
			self.muzzle_right.show(self.x, self.y)

	def set_image(self):
		if self.status == IN_AIR:
			if self.facing == RIGHT:
				self.image = self.game_resources.images['player_jump_right']
			else:
				self.image = self.game_resources.images['player_jump_left']

		elif self.status == ON_GROUND and self.walking == STOP:
			if self.facing == RIGHT:
				self.image = self.game_resources.images['player_stand_right']
			else:
				self.image = self.game_resources.images['player_stand_left']
		else:
			if self.facing == RIGHT:
				self.image = self.game_resources.animations['player_walk_right']
			else:
				self.image = self.game_resources.animations['player_walk_left']

	def update(self, dt):

		if self.walking == LEFT:
			self.velocity_x = -self.default_speed
		elif self.walking == RIGHT:
			self.velocity_x = self.default_speed

		x = int(self.x)
		y = int(self.y)

		#super(Player, self).update(dt)
		self.y += self.velocity_y*dt
		
		on_gorund_flag = False

		for sprite in self.collision_objects:
			if self.collides_with(sprite):

				# kolizja z dołu ( obiekt jest pod playerem )
				if y >= sprite.fixed_y + sprite.height:
					self.y = sprite.fixed_y + sprite.height
					self.velocity_y = 0
					on_gorund_flag = True

					if self.status == IN_AIR:
						self.status = ON_GROUND
						self.set_image()

				# jak nie z dołu to z góry
				elif y + self.height <= sprite.y:
					self.y = sprite.fixed_y - self.height
					self.velocity_y = 0

		if not on_gorund_flag:
			if self.status == ON_GROUND:
				self.status = IN_AIR
				self.set_image()
	

		self.x += self.velocity_x*dt

		for sprite in self.collision_objects:
			if self.collides_with(sprite):
				if x + self.width <= sprite.fixed_x:
					self.x = sprite.fixed_x - self.width
					self.velocity_x = 0

				elif x >= sprite.fixed_x + sprite.width:
					self.x = sprite.fixed_x + sprite.width
					self.velocity_x = 0 

		if self.muzzle_right.visible:
			self.muzzle_right.update(dt, self.x, self.y)
		if self.muzzle_left.visible:
			self.muzzle_left.update(dt, self.x, self.y)


	def on_key_press(self, symbol, modifiers):

	 	if symbol == key.SPACE:
	 		self.fire()
	 	if symbol == key.UP:
	 		self.jump()
	 	if symbol == key.RIGHT:
	 		self.move_right()
	 	if symbol == key.LEFT:
	 		self.move_left()


	def on_key_release(self, symbol, modifiers):

	 	if symbol == key.RIGHT and self.walking == RIGHT :
	 		self.stop()
	 	if symbol == key.LEFT and self.walking == LEFT:
	 		self.stop()

	def draw(self):
	 	super(physicalobject.PhysicalObject, self).draw()

	 	if self.muzzle_left.visible and self.facing == LEFT:
	 		self.muzzle_left.draw()
	 	if self.muzzle_right.visible and self.facing == RIGHT:
	 		self.muzzle_right.draw()