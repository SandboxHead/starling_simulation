import math

def magnitude(x, y, z):
	return math.sqrt((x**2)+(y**2)+(z**2))

def dot(a, b):
	return sum(i*j for i,j in zip(a, b))

def angle_between(a, b):
	angle = math.degrees(math.acos(dot(a, b) / (magnitude(*a) * magnitude(*b))))
	return angle

def limit_magnitude(vector, max_magnitude, min_manitude = 0.0):
	mag = magnitude(*vector)
	if mag > max_magnitude:
		normalizing_factor = max_magnitude / mag
	elif mag < min_magnitude:
		normalizing_factor = min_magnitude /mag
	else: return vector

	return [value * normalizing_factor for value in vector]

def unit_vector(a):
	mag = magnitude(a)
	b = (a[0]/mag, a[1]/mag, a[2]/mag) 
	return b

def bird_orient(vector, bird, size):
	unit_v = unit_vector(vector)

	bird_o = []

	bird_front = ((bird[0]+unit_vector[0]*size[0]), (bird[1]+unit_vector[1]*size[1]), (bird[2]+unit_vector[2]*size[2]))
	bird_left = ((bird[0]+(-unit_vector[2])*size[1]), (bird[1]), (bird[2]+ unit_vector[0]*size[1]))
	bird_right = ((bird[0]+(unit_vector[2])*size[1]), (bird[1]), (bird[2]-unit_vector[0]*size[1]))
	bird_top = (bird[0], (bird[1]+size[3]), bird[2])
	bird_temp=[bird, bird_front, bird_left, bird_right, bird_top]
	return (bird_temp)