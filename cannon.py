# cannon.py

import numpy as np


height = 200
width = 500
tick_scale = 1

gravity = np.array((0, -4, 0, 0))
wind = np.array((1, 0, 0, 0))


def hadamard(c1, c2):
	return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])

def write_pixel(canvas, coords, color):
	try:
		canvas[coords[0], coords[1]] = color
	except IndexError:
		pass

def canvas_to_ppm(canvas):
	out = "P3\n"
	out += "{0} {1}\n".format(canvas.shape[1], canvas.shape[0])
	out += "255\n"
	
	line = ""
	for i in canvas.flat:
		if len(line) >= 66:
			out += line + "\n"
			line = ""
		line += str(int(i*255)) + " "
	out += line + "\n"
	
	with open("ray_tracing.ppm", "w+") as file:
		file.write(out)
	
	return out


class Projectile(object):
	def __init__(self, pos, vel):
		self.pos = np.array(pos)
		self.vel = np.array(vel)
	
	def tick(self):
		return Projectile(
			self.pos + self.vel//tick_scale,
			self.vel + (gravity + wind)//tick_scale)


canvas = np.zeros((height, width, 3))

p = Projectile((0, 10, 0, 1), (50, 30, 0, 0))
count = 0

while p.pos[1] > 0:
	p = p.tick()
	count += 1
	write_pixel(canvas, (height - p.pos[1], p.pos[0]), (1, 0, 0))

canvas_to_ppm(canvas)


