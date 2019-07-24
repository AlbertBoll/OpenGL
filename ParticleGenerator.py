from collections import namedtuple
from pyrr import Vector3, Vector4
from OpenGL.GL import *
import numpy as np

#
# Particle = namedtuple("Particle", "Position Velocity Color Life")
#
#
# Particle = Particle(Position=Vector3([0, 0, 0]),
#                     Velocity=Vector3([0, 0, 0]),
#                     Color=Vector4([1., 1., 1., 1.]),
#                     Life=0.)

class Particle:
    def __init__(self, Position=Vector3([0, 0, 0]), Velocity=Vector3([0, 0, 0]),
                 Color=Vector4([1., 1., 1., 1.]), Life=0.):
        self.Position = Position
        self.Velocity = Velocity
        self.Color = Color
        self.Life = Life

# lastUsedParticle = 0

class ParticleGenerator:
    def __init__(self, shader, texture, amount):
        # Private member data
        self.__shader = shader
        self.__texture = texture
        self.__amount = amount
        self.__particles = []
        self.lastUsedParticle = 0
        self.__init()

    # Public member function
    def Update(self, dt, object_, newParticles, offset):
        for i in range(newParticles):
            unusedParticle = self.__firstUnusedParticle()
            # self.__particles[unusedParticle] = self.__respawnParticle(self.__particles[unusedParticle], object_, offset)
            self.__respawnParticle(self.__particles[unusedParticle], object_, offset)

        for i in range(self.__amount):
            # self.__particles[i] = self.__particles[i]._replace(Life=self.__particles[i].Life-dt)
            self.__particles[i].Life -= dt
            if self.__particles[i].Life > 0.:
                # self.__particles[i] = self.__particles[i]._replace(
                #     Position=self.__particles[i].Position-self.__particles[i].Velocity * dt/2)
                self.__particles[i].Position -= self.__particles[i].Velocity * dt
                self.__particles[i].Color.w -= dt * 2.5
                # r, g, b, alpha = self.__particles[i].Color
                # alpha -= dt * 2
                # self.__particles[i] = self.__particles[i]._replace(Color=Vector4([r, g, b, alpha]))


            # p = self.__particles[i]

            # p.Life -= dt
            # if p.Life > 0.:
            #     p.Position -= p.Velocity * dt
            #     p.Color.w -= dt * 2.5
            # print(self.__particles[i])

    def draw(self):
        # print(1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        self.__shader.Use()
        for particle in self.__particles:
            if particle.Life > 0:
                # print(particle)
                self.__shader.SetVector2f("offset", particle.Position)
                self.__shader.SetVector4f("color", particle.Color)
                glActiveTexture(GL_TEXTURE0)
                self.__texture.Bind()
                glBindVertexArray(self.quadVAO)
                glDrawArrays(GL_TRIANGLES, 0, 6)
                glBindVertexArray(0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Private member function
    def __init(self):
        self.quadVAO = glGenVertexArrays(1)
        glBindVertexArray(self.quadVAO)
        self.quadVBO = glGenBuffers(1)
        data = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0,
                         1.0, 1.0, 1.0, 0.0, 1.0, 0.0], dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * data.itemsize, ctypes.c_void_p(0))
        # glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * data.itemsize, GL_VOID_P(0))
        # glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        for i in range(self.__amount):
            self.__particles.append(Particle())

    def __firstUnusedParticle(self):
        # global lastUsedParticle
        for i in range(self.lastUsedParticle, self.__amount):
            if self.__particles[i].Life <= 0.:
                self.lastUsedParticle = i
                return i

        for i in range(self.lastUsedParticle):
            if self.__particles[i].Life <= 0.:
                self.lastUsedParticle = i
                return i

        self.lastUsedParticle = 0
        return 0

    @staticmethod
    def __respawnParticle(particle, object_, offset=Vector3([0., 0., 0.])):
        random = (np.random.randint(100)-50)/10.
        rColor = 0.5 + np.random.randint(100)/100.
        particle.Position = object_.pos + random + offset
        particle.Color = Vector4([rColor, rColor, rColor, 1.0])
        particle.Life = 1.0
        particle.Velocity = object_.velocity * 0.1
        # Position = object_.pos + random + offset
        # Color = Vector4([rColor, rColor, rColor, 1.0])
        # Life = 1.0
        # Velocity = object_.velocity * 0.1
        # # # global particle
        # particle = particle._replace(Position=Position, Color=Color, Life=Life, Velocity=Velocity)
        # return particle







