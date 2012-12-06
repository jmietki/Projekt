# -*- coding: utf-8 -*-
import xml.etree.ElementTree as elementTree
import os.path

class Config(object):
	""" Klasa bazowa do wszystkich konfiguracji """
	def __init__(self, rootTree = None):
		super(Config, self).__init__()
		self.tree = rootTree

	def get_resources_list(self):
		""" Ważne - zrobić sprawdzanie poprawności konfiguracjii """

		# utworzenie listy przechowującej zasoby do załadowania
		resource_list = list()

		# przeszukanie drzewa i wyszukanie elementów <image/>
		# jeżeli node ma atrybut autoload i jest on ustawiony na true 
		# to zostanie dodany do listy resource_list
		for resource in self.tree.iter('image'):
			resource.attrib['type'] = 'image'
			resource_list.append(resource.attrib)

		# przeszukanie drzewa i wyszukanie elementów <animation>
		for resource in self.tree.iter('animation'):
			frames = list()

			# pobranie wszystkich klatek animacji 
			for frame in resource.findall('frame'):
				frames.append(frame.attrib)

			resource.attrib['type'] = 'animation'
			resource.attrib['frames'] = frames
			resource_list.append(resource.attrib)

		return resource_list



class LevelConfig(Config):
	""" Klasa konfiguracyjna dla levels.xml """
	def __init__(self, path, rootTree = None):
		super(LevelConfig, self).__init__(rootTree)		

		self.path = path

	def get_objects_list(self):

		# lista przechowująca opisy obiektów
		objects_list = list()

		for l_object in self.tree.iter('object'):
			if 'collision' in l_object.attrib and l_object.attrib['collision'].lower() == "false":
				l_object.attrib['collision'] = False
			else:
				l_object.attrib['collision'] = True

			objects_list.append(l_object.attrib)

		return objects_list



class GameConfig(Config):
	""" Klasa konfiguracyjna dla game.xml """

	def __init__(self, rootTree = None):
		super(GameConfig, self).__init__(rootTree)

		# domyślne rozdzielczości - taki fallback
		# w razie gdyby nie było podanej rozdzielczości w pliku konfiguracyjnym 
		self.display_width = 1280
		self.display_height = 720
		self.fullscreen = False

		try:
			display = self.tree.find('display')
			resolution = display.find('resolution')
			fullscreen = display.find('fullscreen')

			self.display_width = int(resolution.get('width'))
			self.display_height = int(resolution.get('height'))

			if fullscreen.get('value').lower() == 'true':
				self.fullscreen = True
		except:
			print "Błąd w pliku konfiguracyjnym"



class ConfigReader():
	""" Generator klas Config """
	def __init__(self):
		pass

	def read(self, filename):
		tree = elementTree.parse(os.path.normpath(filename))
		root = tree.getroot() 

		return root

	def game_config(self, filename):
		config = GameConfig(self.read(filename))
		return config

	def level_config(self, path, filename):
		config = LevelConfig(path, self.read(path+filename))
		return config
