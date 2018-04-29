from pyglet.gl import *
from pyglet.window import key
import math, random
from boid import Boid

class Model:
	def __init__(self, boids):
		self.batch = pyglet.graphics.Batch()

		# color = ('c3f', (1,0.4,0.5,)*4)
		# color2 = ('c3f', (0.5, 0.4, 1)*4)
		# color3 = ('c3f', (1, 0.5, 0.4)*4)
		# color4 = ('c3f', (0.4, 1, 0.5)*4)
		# x,y,z = 0,0,-1
		# X,Y,Z = x+1, y+1, z+1
		# self.faces = []
		# self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (X,y,z, x,y,z, x,Y,z, X,Y,z,)), color )) #back
		# self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (x,y,Z, X,y,Z, X,Y,Z, x,Y,Z,)), color2 )) #front
		# self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (x,y,z, x,y,Z, x,Y,Z, x,Y,z,)), color3 )) #left
		# self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (X,y,Z, X,y,z, X,Y,z, X,Y,Z,)), color4 )) #right
		self.objs = []
		self.vels = []
		for boid in boids:
			x, y, z = boid.position
			c1, c2, c3 = boid.color
			color = ('c3f', (c1, c2, c3)*3)
			self.vels.append(boid.velocity)
			self.objs.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (x,y,z, x+1,y,z, x+0.5, y+1,z,)), color))


		# boid = Boid()
		# pos = boid.position
		# x, y, z = 0, 0, -1
		# c1, c2, c3 = boid.color
		# color = ('c3f', (c1, c2, c3)*3)
		# self.faces = []
		# self.faces.append(self.batch.add(3, GL_TRIANGLES, None, ('v3f', (x,y,z, x+1,y,z, x+0.5, y+1,z, )), color))

	def draw(self):
		for num in range(len(self.objs)):
			obj = self.objs[num]
			vel = self.vels[num]
			for index in range(3):
				# print(obj.vertices[index])
				obj.vertices[index*3+2] = obj.vertices[index*3+2] +vel[2]
				obj.vertices[index*3+1] = obj.vertices[index*3+1] +vel[1]
				obj.vertices[index*3] = obj.vertices[index*3] +vel[0]
				
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
		if self.rot[0]>90 : self.rot[0] = 90
		if self.rot[0]<-90 : self.rot[0] = -90
		if self.rot[1]>90 : self.rot[1] = 90
		if self.rot[1]<-90 : self.rot[1] = -90

	def update(self, dt, keys):
		s = dt*10
		rotY = -self.rot[1]/180*math.pi
		dx, dz = math.sin(rotY), math.cos(rotY)
		if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
		if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
		if keys[key.D]: self.pos[0]-=dz; self.pos[2]-=dx
		if keys[key.A]: self.pos[0]+=dz; self.pos[2]+=dx
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


	def create_boid(self,length, width, height):
		return Boid(position=[random.uniform(-length, length),random.uniform(-width, width),random.uniform(-height-10, 0)],
					velocity=[random.uniform(-0.02,0.02),random.uniform(-0.02,0.02),random.uniform(-0.02,0.02)],
					color=[random.random(), random.random(), random.random()])

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(200, 200)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		self.boids = []
		for n in range(10):
			self.boids.append(self.create_boid(1,1,1))
		self.model = Model(self.boids)
		self.player = Player()
	def on_draw(self):
		self.set3d()
		self.clear()
		self.push(self.player.pos, self.player.rot)	
		x,y,z = self.player.pos
		self.model.draw()
		glPopMatrix()

if __name__ == '__main__':
	window = Window( width=1200, height=700, caption = "Minecraft", resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST)
	pyglet.app.run()