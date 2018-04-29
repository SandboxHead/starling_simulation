import math
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
				color=[0.0, 0.0, 0.0],
				neighbours=[],
				group_average_velocity=[0.0,0.0,0.0],
				group_centre=[0.0,0.0,0.0],
				obj_nearby=[],
				size = [10,7,7]):
			self.size = size
			self.position = position
			self.neighbours = neighbours
			self.velocity = velocity
			self.color = color
			self.force_factors = []

			self.obj_nearby = obj_nearby

	def __repr__(self):
		return "Boid: position={}, velocity={}, color={}".format(
			self.position, self.velocity, self.color)



	def determine_nearby_boids(self, all_boids):
			(self.neighbours).clear()
			for boid in all_boids:
				diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1], boid.position[2] - self.position[2])
				if(boid != self and 
						vector.magnitude(*diff) <= _RANGE_OF_BOID and 
						vector.angle_between(self.velocity, diff) <= _VIEW_ANGLE):
					(self.neighbours).append(boid)
			
