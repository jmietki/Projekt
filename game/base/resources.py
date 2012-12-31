# -*- coding: utf-8 -*-

import pyglet 

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
				self.images[resource['name']] = pyglet.image.load(path+resource['file'])
				if 'flip' in resource:
					self.images[resource['name']].anchor_x = self.images[resource['name']].width/2
					self.images[resource['name']] = self.images[resource['name']].texture.get_transform(True, False, 0)
					self.images[resource['name']].anchor_x = 0
				
			
			if r_type == 'sound':
				pass

			if r_type == 'animation':
				# utworzenie listy klatek
				animation_frames = list()

				for frame in resource['frames']:
					# utworzenie klatki animacji
					image = pyglet.image.load(path+frame['file'])

					if 'flip' in frame:
						image.anchor_x = image.width/2
						image = image.texture.get_transform(True, False, 0)
						image.anchor_x = 0
					if float(frame['time']) == 0:
						frame = pyglet.image.AnimationFrame(image, None) 
					else:
						frame = pyglet.image.AnimationFrame(image, float(frame['time'])) 

					# dodanie do listy klatek
					animation_frames.append(frame)

				animation = pyglet.image.Animation(animation_frames)
				self.animations[resource['name']] = animation

