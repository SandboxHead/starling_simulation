import math
import random

def magnitude(x, y, z):
	return math.sqrt((x**2)+(y**2)+(z**2))

def magnitude2(x, y, z):
	return math.sqrt((x**2)+(z**2))

def dot(a, b):
	return sum(i*j for i,j in zip(a, b))

def dot2(a, b):
	return (a[0]*b[0]+a[2]*b[2])

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c
    
def angle_between(a, b):
	try:
		angle = math.degrees(math.acos(dot2(a, b) / (magnitude2(*a) * magnitude2(*b))))
		return angle
	except:
		return 0


def limit_magnitude(vector, max_magnitude, min_magnitude = 0.0, randomness = False):
	mag = magnitude(*vector)
	if mag > max_magnitude:
		normalizing_factor = max_magnitude / mag
	elif mag < min_magnitude:
		normalizing_factor = min_magnitude /mag
	else: return vector
	if randomness:
		return [(value * normalizing_factor)+random.uniform(-150, 150) for value in vector]
	else:
		return [(value * normalizing_factor) for value in vector]


def unit_vector(a):
	mag = magnitude(a[0], a[1], a[2])
	b = (a[0]/mag, a[1]/mag, a[2]/mag) 
	return b

def bird_orient(f, vector, bird, size):
	unit_v = unit_vector(vector)

	bird_o = []

	bird_front = [bird[0]+unit_v[0]*size[0], bird[1]+unit_v[1]*size[1], bird[2]+unit_v[2]*size[2]]
	bird_left = [(bird[0]+(-unit_v[2])*size[1]), (bird[1]+4*f), (bird[2]+ unit_v[0]*size[1])]
	bird_right = [(bird[0]+(unit_v[2])*size[1]), (bird[1]+4*f), (bird[2]-unit_v[0]*size[1])]
	bird_top = [bird[0], (bird[1]-size[2]), bird[2]]
	bird_temp=[bird, bird_front, bird_left, bird_right, bird_top]
	return (bird_temp)