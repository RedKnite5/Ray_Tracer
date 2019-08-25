# color_canvas.py

import numpy as np

def hadamard(c1, c2):
	return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])

def write_pixel(canvas, coords, color):
	canvas[coords[0], coords[1]] = color

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
	return out


canvas = np.zeros((3, 5, 3))

write_pixel(canvas, (0, 0), (1, 0, 0))
write_pixel(canvas, (1, 2), (0, .5, 0))
write_pixel(canvas, (2, 4), (0, 0, 1))

ppm = canvas_to_ppm(canvas)
print(ppm)

with open("ray_tracing.ppm", "w+") as file:
	file.write(ppm)






