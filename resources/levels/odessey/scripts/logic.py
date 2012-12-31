import os
from base.scripts import IELevelLogic 

class OdesseyLogic(IELevelLogic):
	"""docstring for OdesseyLogic"""
	def __init__(self, objects):
		super(OdesseyLogic, self).__init__()
	
		self.objects = objects


	def update(self, dt):
		for key in self.objects:
			if self.objects[key].rotation <= -360:
				self.objects[key].rotation = 0
			self.objects[key].rotation -= 5