# rays.py

import random as rand
import numpy as np
import matrices as mat


class Ray(object):
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction

		try:
			self.origin = self.origin.reshape((4, 1))
			self.direction = self.direction.reshape((4, 1))
		except:
			if len(origin) == 3:
				self.origin = np.array((*origin, 1))
			if len(direction) == 3:
				self.direction = np.array((*direction, 0))
			
			self.origin = self.origin.reshape((4, 1))
			self.direction = self.direction.reshape((4, 1))
			
		self.shape = (self.origin.shape, self.direction.shape)

	
	def travel(self, time):
		return self.origin + self.direction * time
	
	def __repr__(self):
		return f"Ray({self.origin.tolist()}, {self.direction.tolist()})"
	
	
class Sphere(object):
	def __init__(self, radius, center=(0, 0, 0, 1)):
		self.radius = radius
		self.center = np.array(center)
		self.transform = np.identity(4)
		
		if len(center) == 3:
			self.center = np.array((*center, 1))
	
	def __str__(self):
		return f"Sphere({self.radius}, {tuple(self.center)}"


def intersect(ray, sphere):

	ray = transform(ray, np.linalg.inv(sphere.transform))

	s2r = ray.origin.reshape(4) - sphere.center

	direction = ray.direction.reshape(4)

	a = direction.dot(direction)
	b = 2 * direction.dot(s2r)
	c = s2r.dot(s2r) - sphere.radius

	dis = b*b - 4 * a * c

	if dis >= 0:
		t1 = (-b + dis ** .5)/(2*a)
		t2 = (-b - dis ** .5)/(2*a)
		inters = sorted((t1, t2))
		ret = []
		for i in inters:

			ret.append(Intersection(i, sphere))
		return ret
	else:
		return


def hit(sections):
	h = sections[0]
	for i in sections:
		if 0 < i.t < h.t:
			h = i
	return h


class Intersection(object):
	def __init__(self, t, obj):
		self.t = t
		self.obj = obj
	
	def __repr__(self):
		return f"Intersection({self.t}, {self.obj})"

intersections = []

def transform(r, matrix):
	new_origin = (matrix @ r.origin).astype("float64")
	new_direction = (matrix @ r.direction).astype("float64")
	return Ray(new_origin, new_direction)





if __name__ == "__main__":
	HEIGHT = 200
	WIDTH = 200
	canvas = np.zeros((HEIGHT, WIDTH, 3))

	rays = np.zeros((HEIGHT, WIDTH), dtype=Ray)

	sphere = Sphere(1, (0, 0, 0))

	for i in range(HEIGHT):
		for j in range(WIDTH):
			rays[i, j] = Ray((0, 0, -2), (i - HEIGHT/2, j - WIDTH/2, 30))
			
			intersections = intersect(rays[i, j], sphere)
			if intersections:
				canvas[i, j] = (1, 0, 0)


	mat.canvas_to_ppm(canvas)








