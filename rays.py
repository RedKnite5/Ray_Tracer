# rays.py

import random as rand
import numpy as np
from math import pi

import matrices as mat
import color_canvas as cc

black = np.array((0, 0, 0))

class Ray(object):
	def __init__(self, origin, direction):
		self.origin = make_point(origin)
		self.direction = make_vector(direction)
			
		self.shape = (self.origin.shape, self.direction.shape)

	
	def travel(self, time):
		return self.origin + self.direction * time
	
	def __repr__(self):
		return f"Ray({self.origin.tolist()}, {self.direction.tolist()})"
	

class Material(object):
	__slots__ = ["data"]
	def __init__(self, color=(1, 1, 1), *args):
		try:
			assert len(args) == 4
			assert len(color) == 3
			#assert all(0 <= c <= 1 for c in color)
		
		except AssertionError:
			raise
		
		self.data = dict(zip((
			"color", "ambient", "diffuse", "specular", "shiny"),
			(make_color(color), *args)))
	
	def __getattr__(self, name):
		
		return self.data[name]

	


def make_point(*it):
	if len(it) == 1:
		it = it[0]
	ar = np.array(it) if len(it) == 4 else np.array((*it, 1))
	ar.reshape((4, 1))
	ar = ar.astype("float64")
	return ar

def make_vector(*it):
	if len(it) == 1:
		it = it[0]
	ar = np.array(it) if len(it) == 4 else np.array((*it, 0))
	ar.reshape((4, 1))
	ar = ar.astype("float64")
	return ar

def make_color(*it):
	if len(it) == 1:
		it = it[0]
	if len(it) == 3:
		ar = np.array(it)
	elif len(it) == 1:
		ar = np.ones
		ar * it[0]
	else:
		raise ValueError
	ar = ar.astype("float64")
	return ar


material = Material((1, 1, 1), .1, .9, .9, 200.)

class Sphere(object):
	def __init__(self,
		radius=1,
		center=(0, 0, 0, 1),
		m=material):
		
		self.radius = radius
		self.center = make_point(center)
		self.transform = np.identity(4)
		self.material = m

	
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


def normal_at(sphere, point):
	p = np.linalg.inv(sphere.transform) @ point
	obj_normal = p - sphere.center
	world_normal = (np.transpose(np.linalg.inv(sphere.transform))
		@ obj_normal)
	return normalize(world_normal)


def normalize(point):
	p = make_point(point)
	t = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** .5
	p[:3] = p[:3] / t
	p[3] = 1
	return p

def reflect(incoming, normal):
	return incoming - normal * 2 * np.dot(incoming, normal)


class Light(object):
	__slots__ = ["pos", "intense"]
	def __init__(self, pos, intense):
		self.pos = make_point(pos)
		self.intense = make_color(intense)
	
	def __str__(self):
		return "Light{self.pos, self.intense}"


def lighting(m, l, p, inc, norm):
	
	# This is a dot product. I'm not sure it should be.
	# See page 88
	ec = make_color(m.color,) * make_color(l.intense)
	lightv = normalize(l.pos - make_point(p))
	amb = ec * m.ambient
	l_dot_norm = np.dot(lightv, norm)
	if l_dot_norm < 0:
		diffuse = black # black???
		specular = black # black
	else:
		
		diffuse = ec * material.diffuse * l_dot_norm
		
		reflectv = reflect(-lightv, norm)
		reflect_dot_eye = np.dot(reflectv, inc)
		
		if reflect_dot_eye <= 0:
			specular = black
		else:
			factor = reflect_dot_eye ** m.shiny
			specular = l.intense * m.specular * factor
	
	# print(amb, diffuse, specular)
	return amb + diffuse + specular

if __name__ == "__main__":
	
	l = Light((0, 0, -10), (1, 1, 1))
	r = lighting(
		material, l, (0, 0, 0),
		make_vector(0, 0, -1),
		make_vector(0, 0, -1))
	print("Should be: (1.9, 1.9, 1.9) ", r)
	
	l = Light((0, 0, -10), (1, 1, 1))
	r = lighting(
		material, l, (0, 0, 0),
		make_vector(0, (2**.5)/2, -(2**.5)/2),
		make_vector(0, 0, -1))
	print("Should be: (1, 1, 1) ", r)
	
	l = Light((0, 10, -10), make_color(1, 1, 1))
	r = lighting(
		material,
		l, make_point(0, 0, 0),
		make_vector(0, 0, -1),
		make_vector(0, 0, -1))
	print("Should be: (.7364, .7364, .7364) ", r)
	
	l = Light((0, 10, -10), make_color(1, 1, 1))
	r = lighting(
		material,
		l, make_point(0, 0, 0),
		make_vector(0, -2**-.5, -2**-.5),
		make_vector(0, 0, -1))
	print("Should be: (1.6364, 1.6364, 1.6364) ", r)
	
	l = Light((0, 0, 10), make_color(1, 1, 1))
	r = lighting(
		material,
		l, make_point(0, 0, 0),
		make_vector(0, 0, -1),
		make_vector(0, 0, -1))
	print("Should be: (.1, .1, .1) ", r)
	
	
	# whole sphere:
	ray_origin = make_point(0, 0, -5)
	
	wall_z = 10
	
	wall_size = 7
	
	canvas_pixels = 100
	
	pixel_size = wall_size / canvas_pixels
	
	half = wall_size / 2
	
	canvas = np.zeros((canvas_pixels, canvas_pixels, 3))
	color = make_color(1, 0, 0)
	shape = Sphere()
	
	for y in range(canvas_pixels - 1):
		world_y = half - pixel_size * y
		
		for x in range(canvas_pixels - 1):
			
			world_x = -half + pixel_size * x
			
			position = make_point(world_x, world_y, wall_z)
			
			r = Ray(ray_origin, normalize(position - ray_origin))
			xs = intersect(r, shape)
			print(xs)
			try:
				hits = hit(xs)
				cc.write_pixel(canvas, x, y, color)
			except TypeError:
				pass
	
	ppm = cc.canvas_to_ppm(canvas)
	
	with open("ray_tracing.ppm", "w+") as file:
		file.write(ppm)
			
	








