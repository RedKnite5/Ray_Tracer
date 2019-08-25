# rays.py

import random as rand
import numpy as np
import matrices as mat

m = mat.translation_mat(1, 2, 3)
print(m)

class Ray(object):
	def __init__(self, origin, direction):
		self.origin = tuple(origin)
		self.direction = tuple(direction)
		
		if len(origin) == 3:
			self.origin = (*origin, 1)
		if len(direction) == 3:
			self.direction = (*direction, 0)
	
	def travel(self, time):
		return self.origin + self.direction * time
	
class Sphere(object):
	def __init__(self, radius, center=(0, 0, 0)):
		self.radius = radius
		self.center = center
	
	