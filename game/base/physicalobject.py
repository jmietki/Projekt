# -*- coding: utf-8 -*-
import pyglet
import math

class PhysicalObject(pyglet.sprite.Sprite):
	""" Klasa bazowa dla wszystkich obiektów w grze """

	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)

		# Prędkość
		self.velocity_x, self.velocity_y = 0.0, 0.0
		self.depth = 1

		self.image_anchor_x = self.image.anchor_x
		self.image_anchor_y = self.image.anchor_y

	@property
	def fixed_x(self):
		return self.x - self.image_anchor_x

	@property
	def fixed_y(self):
		return self.y - self.image_anchor_y

	def update(self, dt):
		""" Metoda powinna być wywoływana co klatkę """

		# uaktualnienie pozycji zgodnie z wektorami prędkości
		self.x += self.velocity_x*dt
		self.y += self.velocity_y*dt

	def collides_with_rect(self, obj):
		""" Sprawdzanie czy obiekt koliduje z innym """
		""" Przepisać na rect !!! """
		
		left1 = int(math.floor(self.fixed_x))
		left2 = int(math.floor(obj.fixed_x))
		right1 = left1 + self.width
		right2 = left2 + obj.width
		top1 = int(math.floor(self.fixed_y))
		top2 = int(math.floor(obj.fixed_y))
		bottom1 = top1 + self.height
		bottom2 = top2 + obj.height

		if bottom1 <= top2: 
			return False
		if top1 >= bottom2: 
			return False

		if right1 <= left2: 
			return False
		if left1 >= right2: 
			return False

		return True;


	def __repr__(self):
		""" Na portrzeby sortowania """
		return repr((self.depth))

	def on_collide(self):
		pass

