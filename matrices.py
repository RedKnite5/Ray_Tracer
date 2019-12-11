# matrices.py

import numpy as np
import math

height = 500
width = 500

__all__ = ["Projectile", "hadamard", "write_pixel", "canvas_to_ppm",
"minor", "trans", "scale", "rotate", "shear"]

class Projectile(object):
	def __init__(self, pos, vel):
		self.pos = np.array(pos)
		self.vel = np.array(vel)
	
	def tick(self):
		return Projectile(
			self.pos + self.vel//tick_scale,
			self.vel + (gravity + wind)//tick_scale)


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


def minor(a, i, j):
	b = np.delete(a, 0, i)
	c = np.delete(b, 1, j)
	
	return np.linalg.det(c)

def trans(x, y, z):
	i = np.identity(4)
	i[:, -1] = np.array((x, y, z, 1))
	return i

def scale(x, y, z):
	i = np.identity(4)
	i[np.diag_indices_from(i)] = [x, y, z, 1]
	return i

def rotate(var, r):
	i = np.identity(4)
	
	if var.lower() == "x":
		i[1:-1, 1:-1] = np.array(
			((math.cos(r), -math.sin(r)),
			(math.sin(r), math.cos(r))), dtype= np.float32)
	elif var.lower() == "y":
		i[::2, ::2] = np.array(
			((math.cos(r), math.sin(r)),
			(-math.sin(r), math.cos(r))), dtype= np.float32)
	elif var.lower() == "z":
		i[:2, :2] = np.array(
			((math.cos(r), -math.sin(r)),
			(math.sin(r), math.cos(r))), dtype= np.float32)
	
	return i
	
def shear(xy, xz, yx, yz, zx, zy):
	i = np.identity(4)
	i[0, 1] = xy
	i[0, 2] = xz
	i[1, 0] = yx
	i[1, 2] = yz
	i[2, 0] = zx
	i[2, 1] = zy
	return i



def clock():
	canvas = np.ones((height, width, 3))

	point = (0, -1, 0, 1)
	points = [point]
	for i in range(1,12):
		j = i*math.pi/6
		points.append(rotation_mat("z", j)@point)
	points = np.array(points).reshape(12, 4)

	points[:, :-1] = points[:, :-1] * 200 + 250
	points = np.int16(points)

	for i in points:
		canvas[i[0]-6:i[0]+6, i[1]-6:i[1]+6, :] = (1, 0, 0)

	canvas_to_ppm(canvas)




