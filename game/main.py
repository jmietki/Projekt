#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

import sys, os

from base.configuration import *
from base.physicalobject import *
from base.player import *
from base.resources import *
from base.level import *
from base.camara import *

class Game(pyglet.window.Window):
	"""Główna klasa aplikacji"""

	def __init__(self):

		head, tail = os.path.split(__file__)
		sys.path.append(head)

		# self.config jest zarezerwowane przez pyglet.window.Window
		# więc musi być inna nazwa - game_config
		self.game_config = ConfigReader().game_config('game.xml')

		# Wywołanie konstruktora obiektu rodzica
		if self.game_config.fullscreen:
			super(Game, self).__init__(fullscreen=True)
		else:
			super(Game, self).__init__(self.game_config.display_width, 
				self.game_config.display_height)
			#self.set_exclusive_mouse(True)

		# załadowanie współdzielonych zasobów gry
		self.game_resources = Resources()
		self.game_resources.load(self.game_config.get_resources_list())
 
		# utworzenie gracza 
		self.player = Player(self.game_resources)
		self.player.x = 100
		self.player.y = 500

		# zarejestrowanie playera jako odbierającego eventy
		self.push_handlers(self.player)

		# utworzenie kamery i powiązanie jej z graczem
		self.camera = FlatCamera(self.width, self.height)
		self.camera.bind(self.player)
		self.camera.y = 200

		# utworzenie mapy
		self.level = Level(self.game_resources, self.player, self.camera)

		# przekazanie graczowi informacji o obiektach kolizyjnych,
		self.player.collision_objects = self.level.collision_objects


		# odświeżanie gry z częstotliwością 1/120
		pyglet.clock.schedule_interval(self.update, 1/120.0)

		# numer wersji i fps ;)
		self.label = pyglet.text.Label("v0.09")
		self.label.x = self.width - 50
		self.label.y = 10
		self.fps_display = pyglet.clock.ClockDisplay()
		self.live_level_building = False

	def reload_level(self, dt):
		try:
			level = Level(self.game_resources, self.player, self.camera)
		except Exception, e:
			print e
			pass
		else:
			self.level = level
			self.player.collision_objects = self.level.collision_objects


	def update(self, dt):
		# grawitacja
		self.player.velocity_y -= 1800*dt

		self.player.update(dt)

		# aktualizacja poziomu
		self.level.update(dt)

		if self.player.y < -1500:
			self.player.x = 100
			self.player.y = 500
			self.camera.y = 0
			self.camera.x = 0


	def on_draw(self):
		#pyglet.clock.tick()
		self.clear()

		# update kamery
		self.camera.project()

		# rysowanie poziomu
		# podaje referencje do gracza ponieważ chce rysować warstwami wg depth
		self.level.draw_parallex(self.camera, self.player)

		# rysowanie HUD'a - najpierw wyzerowanie macierzy widoku
		# HUD nie ma się przemieszczać 
		glLoadIdentity()

		self.fps_display.draw()
		self.label.draw()


	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.R:
			if self.live_level_building:
				pyglet.clock.unschedule(self.reload_level)
				self.live_level_building = False
				print "Dynamiczne ładowanie mapy wyłączone"
			else: 
				pyglet.clock.schedule_interval(self.reload_level, 1)
				self.live_level_building = True
				print "Dynamiczne ładowanie mapy włączone"

		if symbol == pyglet.window.key.K:
			self.player.x = 100
			self.player.y = 250
			self.camera.y = 0
			self.camera.x = 0
		elif symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.Q:
			pyglet.app.exit()

if __name__ == '__main__':
	game = Game()
	pyglet.app.run()
