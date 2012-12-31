# -*- coding: utf-8 -*-

from pyglet.gl import *

# Flagi dla określenia w którą strone jest skierowany
LEFT  = 0x01
RIGHT = 0x02
STOP  = 0x04
JUMP  = 0x08
FALL  = 0x16
ON_GROUND = 0x32

class FlatCamera(object):
	""" Implementacja kamery podążającej za graczem

	Atrybuty:
		x, y:       Pozycja kamery.
		viewport_x, 
		viewport_y: Pozycja rzutni. 
		width:      Szerokość rzutni.
		height:     Wysokość rzutni.
		binded_obj: Referencja do obiektu za którym kamera 
			ma podążać.
	"""
	def __init__(self, width, height):
		""" Inicjacja klasy 

		Argumenty:
			width:  oczekiwana szerokość rzutni
			height: oczekiwana wysokość rzutni
		"""

		super(FlatCamera, self).__init__()
		
		self.x = 0
		self.y = 0

		self.width, self.height = width, height

		self.viewport_x = 0
		self.viewport_y = int((self.height-720)/2)
		if self.viewport_y < 0:
			self.viewport_y = 0			

		self.binded_obj = None
		self.height = 720


	def bind(self, obj):
		""" Wiąże ruch kamery z ruchem obiektu 

			Argumenty:
				obj: Obiekt za którym kamerama podążać
		"""
		self.binded_obj = obj


	def project(self):
		""" Uaktualnia pozycje kamery i rzutuje scene """

		offset_x = self.binded_obj.x - self.x
		offset_y = self.binded_obj.y - self.y

		# if self.binded_obj.x + self.binded_obj.width - self.x >= self.width*2/3:
		# 	self.x =  self.binded_obj.x + self.binded_obj.width - self.width*2/3
		# elif self.binded_obj.x - self.x <= self.width/3:
		# 	self.x = self.binded_obj.x - self.width/3

		if offset_x >= self.width*2/5:
			self.x =  self.binded_obj.x - self.width*2/5
		elif offset_x <= self.width/3:
			self.x = self.binded_obj.x - self.width/3

		if self.x < 0:
			self.x = 0

		if offset_y >= self.height*3.5/5:
			self.y = self.binded_obj.y - self.height*3.5/5
		elif offset_y <= self.height/5:
			self.y = self.binded_obj.y -self.height/5
			

		glViewport(self.viewport_x, self.viewport_y, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.width, 0, self.height, -1, 1)
		glMatrixMode(GL_MODELVIEW)