# -*- coding: utf-8 -*-

import pyglet 
from pyglet.gl import *

from resources import *
from configuration import *
from physicalobject import *

class Level(object):
	"""docstring for Level"""
	def __init__(self, game_resources):
		super(Level, self).__init__()
		
		# ścieżka do katalogu z danymi do poziomu
		self.path = "../resources/levels/odessey/"

		# wczytanie pliku konfiguracyjnego poziomu
		self.config = ConfigReader().level_config(self.path, "level.xml")

		# referencja do ogólnych zasobów gry
		self.game_resources = game_resources

		# zasoby dla levelu
		self.resources = Resources()
		self.resources.load(self.config.get_resources_list(), self.path)
		self.resources.images['saw'].anchor_x = self.resources.images['saw'].width/2
		self.resources.images['saw'].anchor_y = self.resources.images['saw'].height/2

		# listy do przechowywania obiektów 
		self.all_objects = list()			# lista wszystkich obiektów
		self.collision_objects = list()		# lista obiektów kolizyjnych
		self.objects = dict()				# słownik obiektów nazwanych, dla celów logiki poziomu

		# dodanie obiektów według opisu w level.xml
		for object_desc in self.config.get_objects_list():

			level_object = PhysicalObject(self.resources.images[object_desc['image']])
			level_object.x = int(object_desc['x'])
			level_object.y = int(object_desc['y'])

			if 'name' in object_desc:
				self.objects[object_desc['name']] = level_object

			if object_desc['collision'] == True:
				self.collision_objects.append(level_object)

			if 'depth' in object_desc:
				depth = float(object_desc['depth'])
				if depth > 0: 
					level_object.depth = 1/(depth+1) 
				elif depth < 0:
					level_object.depth = abs(depth)+1

			if 'opacity' in object_desc:
				level_object.opacity = int(object_desc['opacity'])
				
			self.all_objects.append(level_object)

		# posortowanie all_objects wg depth
		# sortowanie jest możliwe tylko po physical objects
		self.all_objects = sorted(self.all_objects, key=lambda level_object: level_object.depth)

		#interwał dla animacji
		pyglet.clock.schedule_interval(self.animate, 1/120.0)

	def draw(self):
		for sprinte in self.all_objects:
			sprinte.draw()

	def draw_parallex(self, camera, player):
		""" Rysowanie poziomu z uwzględnieniem efektu Parallex Scroll		"""

		# zerujemny macierz widoku - właściwie to macierze jednostkowa
		glLoadIdentity()

		# mała optymalizacja - jeżeli depth obiektu będzie taki sam jak poprzedni
		# nie będzie potrzeby zerowania macierzy i przesuwania widoku
		last_depth = 0 
		player_drawn = False

		for sprite in self.all_objects:
			# pleayera rysujemy po ostatnie warstwie "zerowej" 
			if sprite.depth > 1 and not player_drawn:
				glLoadIdentity()
				glTranslatef(-camera.x, 0, 0)
				player.draw()
				player_drawn = True
			if sprite.depth != last_depth:
				glLoadIdentity()
				glTranslatef(-camera.x*sprite.depth,0,0)
				last_depth = sprite.depth

			sprite.draw()

		# jeżeli nie było warstwy bliższej ekranu i player nie został narysowany
		# to go teraz rysujemy ;)
		if not player_drawn:
			glLoadIdentity()
			glTranslatef(-camera.x, 0, 0)
			player.draw()
			player_drawn = True

	def animate(self, dt):
		for key in self.objects:
			if self.objects[key].rotation <= -360:
				self.objects[key].rotation = 0
			self.objects[key].rotation -= 5