# -*- coding: utf-8 -*-

import pyglet 
from pyglet.gl import *

import imp, os.path

from base.resources import *
from base.configuration import *
from base.physicalobject import *
		
class Saw(PhysicalObject):
	"""docstring for Saw"""
	def __init__(self, *args, **kwargs):
		super(Saw, self).__init__(*args, **kwargs)
		self.player = None

	def on_collide(self):
		self.player.kill()
		
class Level(object):
	"""docstring for Level"""
	def __init__(self, game_resources, player, camera):
		super(Level, self).__init__()
		
		# ścieżka do katalogu z danymi do poziomu
		self.path = "../resources/levels/odessey/"

		# wczytanie pliku konfiguracyjnego poziomu
		self.config = ConfigReader().level_config(self.path, "level.xml")

		# referencja do ogólnych zasobów gry
		self.game_resources = game_resources

		# referencja do playera
		self.player = player

		# referencja do kamery
		self.camera = camera

		# zasoby dla levelu
		self.resources = Resources()
		self.resources.load(self.config.get_resources_list(), self.path)
		self.resources.images['saw'].anchor_x = self.resources.images['saw'].width/2
		self.resources.images['saw'].anchor_y = self.resources.images['saw'].height/2

		# listy do przechowywania obiektów 
		self.all_objects = list()			# lista wszystkich obiektów
		self.collision_objects = list()		# lista obiektów kolizyjnych
		self.objects = dict()				# słownik obiektów nazwanych, dla celów logiki poziomu

		# wczytanie "skryptów" 
		for script_desc in self.config.get_scripts_list():
			self.scritps = imp.load_source('logic', os.path.normpath(self.path+'scripts/logic.py'))
		
		self.logic = self.scritps.OdesseyLogic(self.objects)


		# dodanie obiektów według opisu w level.xml
		for object_desc in self.config.get_objects_list():

			level_object = None
			if 'class' in object_desc:
				level_object = globals()[object_desc['class']](self.resources.images[object_desc['image']])
				level_object.x = int(object_desc['x'])
				level_object.y = int(object_desc['y'])
				level_object.player = self.player
			else:
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

	def draw(self):
		for sprinte in self.all_objects:
			sprinte.draw()

	def draw_parallex(self, camera, player):
		""" Rysowanie poziomu z uwzględnieniem efektu Parallex Scrolling
		"""

		# zerujemny macierz widoku - właściwie to macierz jednostkowa
		glLoadIdentity()

		# mała optymalizacja - jeżeli depth obiektu będzie taki sam jak poprzedni
		# nie będzie potrzeby zerowania macierzy i przesuwania widoku
		last_depth = 0 
		player_drawn = False

		for sprite in self.all_objects:
			# pleayera rysujemy po ostatnie warstwie "zerowej" 
			if sprite.depth > 1 and not player_drawn:
				glLoadIdentity()
				glTranslatef(-camera.x, -camera.y, 0)
				player.draw()
				player_drawn = True
			if sprite.depth != last_depth:
				glLoadIdentity()
				glTranslatef(-camera.x*sprite.depth,-camera.y*sprite.depth,0)
				last_depth = sprite.depth

			sprite.draw()

		# jeżeli nie było warstwy bliższej ekranu i player nie został narysowany
		# to go teraz rysujemy ;)
		if not player_drawn:
			glLoadIdentity()
			glTranslatef(-camera.x, 0, 0)
			player.draw()
			player_drawn = True

	def update(self, dt):
		self.logic.update(dt)