import math
import random
from pyglet.gl import( 
	glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex3f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)

import vector

_RANGE_OF_BOID = 200.0
_VIEW_ANGLE = 110
_BOID_COLLISION_DISTANCE = 30.0
_MIN_OBSTACLE_DISTANCE = 250.0
_COLLISION_VELOCITY_MAX = 1.0

_SPEED_MAX = 35000.0
_SPEED_MIN = 20000.0


_FACTOR_COHESION = 0.9
_FACTOR_ALIGNMENT = 0.045
_FACTOR_BOID_AVOIDANCE = 7.5
_FACTOR_OBSTACLE_AVOID = 300.0
_FACTOR_ATTRACT = 0.035
_FACTOR_BOUND = 0.0008

class Boid:
	def __init__(self,
				position=[100.0, 100.0, 100.0],
				bounds=[200, 5, 200],
				velocity=[0.0, 0.0, 0.0],
				color=[0.0, 0.0, 0.0],
				neighbours=[],
				group_average_velocity=[0.0,0.0,0.0],
				group_centre=[0.0,0.0,0.0],
				obj_nearby=[],
				size = [10,7,7],
				factor_bound = [0,0,0],
				fly = random.randint(0, 1)):
			self.factor_bound = factor_bound
			self.bound = bounds
			self.size = size
			self.position = position
			self.neighbours = neighbours
			self.velocity = velocity
			self.color = color
			self.force_factors = []
			self.dt = 1
			self.mass = 0.1
			self.force = 0
			self.ang_mom = 0
			self.energy = 0
			if fly==0:
				self.fly = -1
			else:
				self.fly =1

			self.obj_nearby = obj_nearby

	def __repr__(self):
		return "Boid: position={}, velocity={}, color={}".format(
			self.position, self.velocity, self.color)

	def render_velocity(self):
		glColor3f(0.6, 0.6, 0.6)
		glBegin(GL_LINES)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(_RANGE_OF_BOID, 0.0, 0.0)
		glEnd()

	def render_view(self):
		return None

	def render_change_vectors(self):
		return None

	def render_boid(self):
		return None


	def draw(self, show_velocity, show_veiw, show_vectores):
		return None

	def determine_nearby_boids(self, all_boids):
			(self.neighbours).clear()
			for boid in all_boids:
				diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1], boid.position[2] - self.position[2])
				if(boid != self and 
						vector.magnitude(*diff) <= _RANGE_OF_BOID and 
						vector.angle_between(self.velocity, diff) <= _VIEW_ANGLE):
					(self.neighbours).append(boid)
			
	def all_in_one(self):
		if len(self.neighbours) >0:
			c = [0.0, 0.0, 0.0]
			sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
			sum_x1, sum_y1, sum_z1 = 0.0, 0.0, 0.0
			for boid in self.neighbours:
				sum_x += boid.position[0]
				sum_y += boid.position[1]
				sum_z += boid.position[2]

				sum_x1 += boid.velocity[0]
				sum_y1 += boid.velocity[1]
				sum_z1 += boid.velocity[2]

				diff = boid.position[0] - self.position[0], boid.position[1] - self.position[1], boid.position[2] - self.position[2]
				inv_sqr_magnitude = 1/((vector.magnitude(*diff)- self.size[0])**4)
				c[0] = c[0] - inv_sqr_magnitude*diff[0]
				c[1] = c[1] - inv_sqr_magnitude*diff[1]
				c[2] = c[2] - inv_sqr_magnitude*diff[2]
			average_x, average_y, average_z = (sum_x/len(self.neighbours), sum_y/len(self.neighbours), sum_z/len(self.neighbours))
			out = [[average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]]]

			average_x, average_y, average_z = (sum_x1/len(self.neighbours), sum_y1/len(self.neighbours), sum_z1/len(self.neighbours))
			out.append([average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]])
			out.append(vector.limit_magnitude(c, _COLLISION_VELOCITY_MAX,True))
			return out
		else:
			return [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]


	def average_position(self):
		if len(self.neighbours) >0:
			sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
			for boid in self.neighbours:
				sum_x += boid.position[0]
				sum_y += boid.position[1]
				sum_z += boid.position[2]
			average_x, average_y, average_z = (sum_x/len(self.neighbours), sum_y/len(self.neighbours), sum_z/len(self.neighbours))
			return [average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]]
			# print (group_centre)
			# return group_centre

		else:
			return [0.0, 0.0, 0.0]

	def average_velocity(self):
		if len(self.neighbours) >0:
			sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
			for boid in self.neighbours:
				sum_x += boid.velocity[0]
				sum_y += boid.velocity[1]
				sum_z += boid.velocity[2]

			average_x, average_y, average_z = (sum_x/len(self.neighbours), sum_y/len(self.neighbours), sum_z/len(self.neighbours))
			return [average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]]		
		else:
			return [0.0, 0.0, 0.0]
		

	def nearby_obj(self, objs, _MIN_OBSTACLE_DISTANCE):
		self.obj_nearby = [
			obj for obj in objs
			if ( vector.magnitude(obj.position[0] - self.position[0],
									obj.position[1] - self.position[1],
									obj.position[2] - self.position[2]) <= _MIN_OBSTACLE_DISTANCE)]


	def avoid_collisions(self, objs, collision_distance):
		c = [0.0, 0.0, 0.0]
		for obj in objs:
			diff = obj.position[0] - self.position[0], obj.position[1] - self.position[1], obj.position[2] - self.position[2]
			inv_sqr_magnitude = 1/((vector.magnitude(*diff)- self.size[0])**2)

			c[0] = c[0] - inv_sqr_magnitude*diff[0]
			c[1] = c[1] - inv_sqr_magnitude*diff[1]
			c[2] = c[2] - inv_sqr_magnitude*diff[2]
		return vector.limit_magnitude(c, _COLLISION_VELOCITY_MAX)

	#attractors are not affected by distance, so they have a fix effect.
	def attraction(self, attractors): 
		a = [0.0, 0.0, 0.0]

		if(len(attractors)==0):
			return a

		for attractor in attractors:
			a[0] += attractor.position[0] - self.position[0]
			a[1] += attractor.position[1] - self.position[1]
			a[2] += attractor.position[1] - self.position[2]

		return a


	def know_bound(self):
		fact_bound = [0.0, 0.0, 0.0]
		for i in range(3):
			if(self.position[i]>self.bound[i] or self.position[i] < -self.bound[i]):
				fact_bound[i] = (self.bound[i]-self.position[i] )*abs(self.velocity[i])
		return fact_bound

	def update(self, delta, all_boids, attractors, obstacles):
		#start with determining nearby boids.
		self.determine_nearby_boids(all_boids)

		# obstacles = self.nearby_obj(objs, _MIN_OBSTACLE_DISTANCE)
		self.nearby_obj(obstacles, _MIN_OBSTACLE_DISTANCE)
		#initializing all the change vectors
		# cohesion_factor = self.average_position()
		# alignment_factor = self.average_velocity()
		# seperation_factor = self.avoid_collisions(self.neighbours, _BOID_COLLISION_DISTANCE)
		p = self.all_in_one()
		cohesion_factor = p[0]
		alignment_factor = p[1]
		seperation_factor = p[2]
		collision_factor = self.avoid_collisions(self.obj_nearby, _MIN_OBSTACLE_DISTANCE)
		attraction_factor = self.attraction(attractors)
		bound_factor = self.know_bound()

		self.force_factors = [
			[_FACTOR_COHESION, cohesion_factor],
			[_FACTOR_ALIGNMENT, alignment_factor],
			[_FACTOR_BOID_AVOIDANCE, seperation_factor],
			[_FACTOR_OBSTACLE_AVOID, collision_factor],
			[_FACTOR_ATTRACT, attraction_factor],
			[_FACTOR_BOUND, bound_factor]]
		# print(_FACTOR_COHESION)
		# print(cohesion_factor)
		# y = _FACTOR_COHESION*cohesion_factor[0]
		for x in self.force_factors:
			self.velocity[0] += x[1][0]*x[0] 
			self.velocity[1] += x[0] *x[1][1]*0.2
			self.velocity[2] += x[0] *x[1][2]

		velocity2 = vector.limit_magnitude(self.velocity, _SPEED_MAX, _SPEED_MIN, True)

		#changing the boids position in accordance with velocity.
		for i in range(0, len(self.position)):
			self.position[i] += delta*velocity2[i]
			# if (self.position[i] > self.bound[i]) or (self.position[i]< -self.bound[i]):
			# 	self.position[i] = -self.position[i]

		# for i in range(3):
		# 	if (self.position[i] > self.bound[i]) or (self.position[i]< -self.bound[i]):
		# 		self.position = vector.limit_magnitude(self.position, self.bound[i], -self.bound[i], True)				

		self.force = self.mass*vector.magnitude(self.velocity[0]-velocity2[0],self.velocity[1]-velocity2[1],self.velocity[2]-velocity2[2])/(self.dt*50)
		self.velocity = velocity2
		cross = vector.cross(self.velocity, self.position)
		self.ang_mom = self.mass*vector.magnitude(cross[0],cross[1],cross[2])/1000
		self.energy = self.mass*(vector.magnitude(self.velocity[0],self.velocity[1],self.velocity[2])**2)/4000000

def velocity_print(a):
	print (a.velocity[0], a.velocity[1], a.velocity[2])

if __name__ == '__main__':
	chidiya = Boid()
	velocity_print(chidiya)

