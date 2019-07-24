from OpenGL.GL import *
import pyrr
import numpy as np
from math import radians

class SpriteRender:
    def __init__(self, shader):
        self.shader = shader
        self.initRenderData()
        # self.quadVAO = glGenVertexArrays(1)

    def DrawSprite(self, texture, position, size, rotation, color):
        # glBindVertexArray(self.quadVAO)
        # self.quadVAO = glGenVertexArrays(1)
        # glBindVertexArray(self.quadVAO)
        self.shader.Use()
        model = pyrr.matrix44.create_from_translation([-0.5*size.x, -0.5*size.y, 0.])
        scale = pyrr.matrix44.create_from_scale([size.x, size.y, 1.])
        model = np.dot(scale, model)
        rotation = pyrr.matrix44.create_from_axis_rotation([0., 0., 1.], radians(rotation))
        model = np.dot(model, rotation)
        translation_back = pyrr.matrix44.create_from_translation([0.5*size.x, 0.5*size.y, 0.])
        model = np.dot(model, translation_back)
        translation_last = pyrr.matrix44.create_from_translation([position.x, position.y, 0])
        model = np.dot(model, translation_last)
        self.shader.SetMatrix4("model", model)
        self.shader.SetVector3f("spriteColor", color)
        # glBindVertexArray(self.quadVAO)
        glActiveTexture(GL_TEXTURE0)
        texture.Bind()
        glBindVertexArray(self.quadVAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        # glDeleteVertexArrays(1, self.quadVAO)
        # glDeleteBuffers(1, self.quadVBO)

    def initRenderData(self):
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
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def Delete(self):
        glDeleteVertexArrays(1, self.quadVAO)
        glDeleteBuffers(1, self.quadVBO)









