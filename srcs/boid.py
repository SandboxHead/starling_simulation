import math
from pyglet.gl import( 
	glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex3f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)

import vector

_RANGE_OF_BOID = 100.0
_VIEW_ANGLE = 110
_BOID_COLLISION_DISTANCE = 50.0
_MIN_OBSTACLE_DISTANCE = 250.0
_COLLISION_VELOCITY_MAX = 1.0

_SPEED_MAX = 150.0
_SPEED_MIN = 20.0


_FACTOR_COHESION = 0.03
_FACTOR_ALIGNMENT = 0.045
_FACTOR_BOID_AVOIDANCE = 7.5
_FACTOR_OBSTACLE_AVOID = 300.0
_FACTOR_ATTRACT = 0.035

class Boid:
	def __init__(self,
				position=[100.0, 100.0, 100.0],
				bounds=[1000, 1000, 1000],
				velocity=[0.0, 0.0, 0.0],
				color=[1.0, 1.0, 1.0],
				neighbours=[],
				group_average_velocity=[0.0,0.0,0.0],
				group_centre=[0.0,0.0,0.0],
				obj_nearby=[]):

			self.position = position

			self.velocity = velocity
			self.color = color
			self.force_factors = []

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
			return


	def average_position(self):
		if len(self.neighbours) >0:
			sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
			for boid in self.neighbours:
				sum_x += boid.position[0]
				sum_y += boid.position[1]
				sum_z += boid.position[2]
			average_x, average_y, average_z = (sum_x/len(self.neighbours), sum_y/len(self.neighbours), sum_z/len(self.neighbours))
			self.group_centre = [average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]]
			return
		else:
			self.group_centre = [0.0, 0.0, 0.0]
			return

	def average_velocity(self):
		if len(self.neighbours) >0:
			sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
			for boid in self.neighbours:
				sum_x += boid.velocity[0]
				sum_y += boid.velocity[1]
				sum_z += boid.velocity[2]

			average_x, average_y, average_z = (sum_x/len(self.neighbours), sum_y/len(self.neighbours), sum_z/len(self.neighbours))
			self.group_average_velocity = [average_x-self.position[0], average_y-self.position[1], average_z-self.position[2]]
			return		
		else:
			self.group_average_velocity = [0.0, 0.0, 0.0]
			return

	def nearby_obj(self, objs, _MIN_OBSTACLE_DISTANCE):
		self.nearby_obj = (
			obj for obj in objs
			if ( vector.magnitude(obj.position[0] - self.position[0],
									obj.position[1] - self.position[1],
									obj.position[2] - self.position[2]) <= _MIN_OBSTACLE_DISTANCE))
		return

	def avoid_collisions(self, objs, collision_distance):
		c = [0.0, 0.0, 0.0]
		for obj in objs:
			diff = obj.position[0] - self.position[0], obj.position[1] - self.position[1], obj.position[2] - self.position[2]
			inv_sqr_magnitude = 1/((vector.magnitude(*diff)- self.size)**2)

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


	def update(self, delta, all_boids, attractors, obstacles):
		#start with determining nearby boids.
		self.determine_nearby_boids(all_boids)

		# obstacles = self.nearby_obj(objs, _MIN_OBSTACLE_DISTANCE)

		#initializing all the change vectors
		cohesion_factor = self.average_position(),
		alignment_factor = self.average_velocity(),
		seperation_factor = self.avoid_collisions(self.neighbours, _BOID_COLLISION_DISTANCE),
		collision_factor = self.avoid_collisions(obstacles, _MIN_OBSTACLE_DISTANCE)
		attraction_factor = self.attraction(attractors)

		self.force_factors = [
			(_FACTOR_COHESION, cohesion_factor),
			(_FACTOR_ALIGNMENT, alignment_factor),
			(_FACTOR_BOID_AVOIDANCE, seperation_factor),
			(_FACTOR_OBSTACLE_AVOID, collision_factor),
			(_FACTOR_ATTRACT, attraction_factor)]

		for factor, effect in self.force_factors:
			self.velocity[0] += factor*effect[0]
			self.velocity[1] += factor*effect[1]
			self.velocity[2] += factor*effect[2]

		self.velocity = vector.limit_magnitude(self.velocity, _SPEED_MAX, _SPEED_MIN)

		#changing the boids position in accordance with velocity.
		for i in range(0, len(self.position)):
			self.position[i] += delta*self.velocity[i]

def velocity_print(a):
	print (a.velocity[0], a.velocity[1], a.velocity[2])

if __name__ == '__main__':
	chidiya = Boid()
	velocity_print(chidiya)

