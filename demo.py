from pyglet.gl import *
from pyglet.window import key
import math

class Model:
	def __init__(self):
		self.batch = pyglet.graphics.Batch()
		color = ('c3f', (1,0.4,0.5,)*4)
		color2 = ('c3f', (0.5, 0.4, 1)*4)
		color3 = ('c3f', (1, 0.5, 0.4)*4)
		color4 = ('c3f', (0.4, 1, 0.5)*4)
		x,y,z = 0,0,-1
		X,Y,Z = x+1, y+1, z+1
		self.faces = []
		self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (X,y,z, x,y,z, x,Y,z, X,Y,z,)), color )) #back
		self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (x,y,Z, X,y,Z, X,Y,Z, x,Y,Z,)), color2 )) #front
		self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (x,y,z, x,y,Z, x,Y,Z, x,Y,z,)), color3 )) #left
		self.faces.append(self.batch.add(4, GL_QUADS, None, ('v3f', (X,y,Z, X,y,z, X,Y,z, X,Y,Z,)), color4 )) #right



	def draw(self):
		for obj in self.faces:
			for index in range(len(obj.vertices)):
				obj.vertices[index] = obj.vertices[index] +0.005
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


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(200, 200)
		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		self.model = Model()
		self.player = Player()
	def on_draw(self):
		self.set3d()
		self.clear()
		self.push(self.player.pos, self.player.rot)	
		x,y,z = self.player.pos
		self.model.draw()
		glPopMatrix()

if __name__ == '__main__':
	window = Window( width=400, height=300, caption = "Minecraft", resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST)
	pyglet.app.run()