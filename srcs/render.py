from pyglet.gl import *
from pyglet.window import key
import math, random, vector
from boid import Boid
import multiprocessing


class Model:
	def create_boid(self,length, width, height):
		return Boid(position=[random.uniform(-length, length),random.uniform(-width, width),random.uniform(-height-10, 0)],
					velocity=[random.uniform(3000,5000),random.uniform(-500,500),random.uniform(3000,5000)],
					color=[random.random(),random.random(),random.random()])

	def __init__(self):
		self.batch = pyglet.graphics.Batch()
		self.objs = []
		self.boids = []
		for n in range(200):
			self.boids.append(self.create_boid(200,50,200))

		for boid in self.boids:
			x, y, z = boid.position
			c1, c2, c3 = boid.color
			color = ('c3f', (c1, c2, c3)*3)
			vel = boid.velocity
			# x1, y1, z1, x2, y2, z2, x3, y3, z3 = x/10+0.5,y/10,z/10, x/10-0.5,y/10,z/10, x/10, y/10,z/10-2

			p = vector.bird_orient(boid.velocity, boid.position, [20, 5, 5])



			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (p[1][0]/10,p[1][1]/10,p[1][2]/10,p[2][0]/10,p[2][1]/10,p[2][2]/10,p[3][0]/10,p[3][1]/10,p[3][2]/10,)), color))
			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (p[0][0]/10,p[0][1]/10,p[0][2]/10,p[1][0]/10,p[1][1]/10,p[1][2]/10,p[4][0]/10,p[4][1]/10,p[4][2]/10,)), color))

		# boid = Boid()
		# pos = boid.position
		# x, y, z = 0, 0, -1
		# c1, c2, c3 = boid.color
		# color = ('c3f', (c1, c2, c3)*3)
		# self.faces = []
		# self.faces.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (x,y,z, x+1,y,z, x+0.5, y+1,z, )), color))
	def update_boid(self, start, stop):
		for ind in range(start, stop):
			self.boids[ind].update(0.0003, self.boids, [],[])
	def draw(self):
		# for n in range(0, len(self.boids), 100):
		# 	stop = n+100 if n +100 <= len(self.boids) else len(self.boids)
		# 	p = multiprocessing.Process(target = self.update_boid, args = (n, stop))
		# 	p.start()
		for boid in self.boids:
			boid.update(0.0003, self.boids, [],[])
		for num in range(len(self.objs)//2):
			obj = self.objs[num*2]
			obj1 = self.objs[num*2+1]
			boid = self.boids[num]
			x, y, z = boid.position
			p = vector.bird_orient(boid.velocity, boid.position, [20, 5, 5])

			obj.vertices = [p[1][0]/10,p[1][1]/10,p[1][2]/10,p[2][0]/10,p[2][1]/10,p[2][2]/10,p[3][0]/10,p[3][1]/10,p[3][2]/10]
			obj1.vertices = [p[0][0]/10,p[0][1]/10,p[0][2]/10,p[1][0]/10,p[1][1]/10,p[1][2]/10,p[4][0]/10,p[4][1]/10,p[4][2]/10]

			# print(obj.vertices)
		self.batch.draw()

class Player:
	def __init__(self):
		self.pos = [0,0,0]
		self.rot = [0,0]

	def mouse_motion(self, dx, dy):
		dx/=8
		dy/=8
		self.rot[0]+=dy
		self.rot[1]-=dx
		# if self.rot[0]>90 : self.rot[0] = 90
		# if self.rot[0]<-90 : self.rot[0] = -90
		# if self.rot[1]>90 : self.rot[1] = 90
		# if self.rot[1]<-90 : self.rot[1] = -90

	def update(self, dt, keys):
		s = dt*10
		rotY = -self.rot[1]/180*math.pi
		dx, dz = math.sin(rotY), math.cos(rotY)
		if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
		if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
		if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
		if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx
		if keys[key.SPACE]: self.pos[1]+=s
		if keys[key.LSHIFT]: self.pos[1]-=s

class Window(pyglet.window.Window):
	def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
	def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()



	def set3d(self):
		self.Projection()
		gluPerspective(50, self.width/self.height, 0.05, 1000)
		self.Model()


	def setLock(self, state): self.lock = state; self.set_exclusive_mouse(state)
	lock = False
	mouse_lock = property(lambda self:self.lock, setLock)

	def on_mouse_motion(self, x, y, dx, dy):
		if self.mouse_lock: self.player.mouse_motion(dx, dy)


	def on_key_press(self, KEY, MOD):
		if (KEY == key.ESCAPE): self.close()
		if KEY == key.E : self.mouse_lock = not self.mouse_lock

	def update(self, dt):
		self.player.update(dt, self.keys)

	def push(self, pos, rot):
		glPushMatrix();
		glRotatef(-rot[0], 1, 0, 0);
		glRotatef(-rot[1], 0, 1, 0);
		glTranslatef(-pos[0], -pos[1], -pos[2])


	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(200, 200)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		# self.boids = []
		# # for n in range(3000):
		# # 	self.boids.append(self.create_boid(5,5,5))
		self.model = Model()
		self.player = Player()
	def on_draw(self):
		self.set3d()
		self.clear()
		self.push(self.player.pos, self.player.rot)	
		x,y,z = self.player.pos
		# for boid in self.boids:
		# 	boid.update(1, self.boids, [], [])
		# upd = [x.position for x in self.boids]
		self.model.draw()
		glPopMatrix()

if __name__ == '__main__':
	window = Window( width=1900, height=1000, caption = "Minecraft", resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST)
	# ps = []
	# for x in range

	# pyglet.graphics.draw(50000, pyglet.gl.GL_LINE_LOOP, ('v3f', ps, 'c3f', (0,0,0)*50000) )
	pyglet.app.run()