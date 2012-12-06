# -*- coding: utf-8 -*-

import pyglet 
import os.path

class Resources(object):
	"""docstring for Resources"""

	def __init__(self):
		super(Resources, self).__init__()

		self.images = dict()
		self.sounds = dict()
		self.animations = dict()

	def  load(self, resourceList, path=None):
		""" Funkcja ładująca zasoby na podstawie listy w formacie:
			{'type': typ, 'name': nazwa zasobu, 'file': ścieżka}

			Dopuszczalne type zasobów to: image, sound, animation
			path - do ładowania leveli - ścieżka do katalogu z levelem
		"""
		if path is None:
			path = ""

		for resource in resourceList:
			# ładowanie po odpowienich typach
			r_type = resource['type'].lower()
			
			if r_type == 'image':
				self.images[resource['name']] = pyglet.image.load(os.path.normpath(path+resource['file']))
			
			if r_type == 'sound':
				pass

			if r_type == 'animation':
				# utworzenie listy klatek
				animation_frames = list()

				for frame in resource['frames']:
					# utworzenie klatki animacji
					image = pyglet.image.load(os.path.normpath(path+frame['file']))
					frame = pyglet.image.AnimationFrame(image, float(frame['time'])) 

					# dodanie do listy klatek
					animation_frames.append(frame)

				animation = pyglet.image.Animation(animation_frames)
				self.animations[resource['name']] = animation

