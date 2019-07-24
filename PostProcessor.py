from OpenGL.GL import *
import numpy as np
from breakout.data_exporter import vertices
from breakout.Texture2D import Texture2D

class PostProcessing:

    def __init__(self, shader, width, height, Confuse=GL_FALSE , Chaos=GL_FALSE, Shake=GL_FALSE):
        self.PostProcessingShader = shader
        self.texture = Texture2D()
        self.width = width
        self.height = height
        self.Confuse = Confuse
        self.Chaos = Chaos
        self.Shake = Shake
        self.__MSFBO = glGenFramebuffers(1)
        self.__FBO = glGenFramebuffers(1)
        self.__RBO = glGenRenderbuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.__MSFBO)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__RBO)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 8, GL_RGB, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, self.__RBO)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR::POSTPROCESSOR: Failed to initialize MSFBO")
        # glViewport(0, 0, width, height)
        # self.texture.Generate_(width, height, None)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__FBO)

        self.texture.Generate_(width, height, None)
        # self.texture.Generate_(1980, 1200, None)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.ID, 0)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR::POSTPROCESSOR: Failed to initialize FBO")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.__initRenderData()
        self.PostProcessingShader.Use()
        self.PostProcessingShader.SetInteger("scene", 0)

        offset = 1.0 / 300.0
        offsets_arr = [(-offset, offset), (0., offset), (offset, offset), (-offset, 0.), (0.0, 0.0), (offset,  0.0),
                       (-offset, -offset), (0.0, -offset), (offset, -offset)]
        glUniform2fv(glGetUniformLocation(self.PostProcessingShader.ID, "offsets"), 9, offsets_arr)

        edge_kernel = np.array([-1, -1, -1,
                                -1,  8, -1,
                                -1, -1, -1], dtype=np.uint)
        glUniform1iv(glGetUniformLocation(self.PostProcessingShader.ID, "edge_kernel"), 9, edge_kernel)

        blur_kernel = np.array([1.0 / 16, 2.0 / 16, 1.0 / 16,
                                2.0 / 16, 4.0 / 16, 2.0 / 16,
                                1.0 / 16, 2.0 / 16, 1.0 / 16])
        glUniform1fv(glGetUniformLocation(self.PostProcessingShader.ID, "blur_kernel"), 9, blur_kernel)

        # self.__VAO = glGenVertexArrays(1)

        self.__initRenderData()

    # Private member function
    def __initRenderData(self):
        self.__VAO = glGenVertexArrays(1)
        glBindVertexArray(self.__VAO)
        VBO = glGenBuffers(1)
        data = vertices
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * data.itemsize, ctypes.c_void_p(0))
        # glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * data.itemsize, GL_VOID_P(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Public Member function
    def Init(self, width, height):
        # self.PostProcessingShader = shader
        # self.texture = Texture2D()
        self.width = width
        self.height = height
        # # self.Confuse = Confuse
        # # self.Chaos = Chaos
        # # self.Shake = Shake
        # self.__MSFBO = glGenFramebuffers(1)
        # self.__FBO = glGenFramebuffers(1)
        # self.__RBO = glGenRenderbuffers(1)
        # #
        #glViewport(0, 0, width, height)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__MSFBO)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__RBO)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_RGB, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, self.__RBO)
        # if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        #     print("ERROR::POSTPROCESSOR: Failed to initialize MSFBO")
        #glViewport(0, 0, width, height)
        self.texture.Generate_(width, height, None)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__FBO)

        # self.texture.Generate_(width, height, None)
        # self.texture.Generate_(1980, 1200, None)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.ID, 0)
        # if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        #     print("ERROR::POSTPROCESSOR: Failed to initialize FBO")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # self.__initRenderData()
        # self.PostProcessingShader.Use()
        # self.PostProcessingShader.SetInteger("scene", 0)
        #
        # offset = 1.0 / 300.0
        # offsets_arr = [(-offset, offset), (0., offset), (offset, offset), (-offset, 0.), (0.0, 0.0), (offset, 0.0),
        #                (-offset, -offset), (0.0, -offset), (offset, -offset)]
        # glUniform2fv(glGetUniformLocation(self.PostProcessingShader.ID, "offsets"), 9, offsets_arr)
        #
        # edge_kernel = np.array([-1, -1, -1,
        #                         -1, 8, -1,
        #                         -1, -1, -1], dtype=np.uint)
        # glUniform1iv(glGetUniformLocation(self.PostProcessingShader.ID, "edge_kernel"), 9, edge_kernel)
        #
        # blur_kernel = np.array([1.0 / 16, 2.0 / 16, 1.0 / 16,
        #                         2.0 / 16, 4.0 / 16, 2.0 / 16,
        #                         1.0 / 16, 2.0 / 16, 1.0 / 16])
        # glUniform1fv(glGetUniformLocation(self.PostProcessingShader.ID, "blur_kernel"), 9, blur_kernel)

        # self.__VAO = glGenVertexArrays(1)

        # self.__initRenderData()



    def BeginRender(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.__MSFBO)
        # glViewport(0, 0, self.width, self.height)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def EndRender(self):
        # glViewport(0, 0, 1980, 1200)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.__MSFBO)
        # glViewport(0, 0, self.width, self.height)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.__FBO)
        # glViewport(0, 0, self.width, self.height)
        glBlitFramebuffer(0, 0, self.width, self.height, 0, 0, self.width, self.height, GL_COLOR_BUFFER_BIT, GL_NEAREST)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)  # Binds both READ and WRITE framebuffer to default framebuffer

    def Render(self, time):
        # glViewport(0, 0, self.width, self.height)
        # glClear(GL_COLOR_BUFFER_BIT)
        # glViewport(0, 0, self.width, self.height)
        self.PostProcessingShader.Use()
        self.PostProcessingShader.Setfloat("time", time)
        self.PostProcessingShader.SetInteger("confuse", self.Confuse)
        self.PostProcessingShader.SetInteger("shake", self.Shake)
        self.PostProcessingShader.SetInteger("chaos", self.Chaos)

        # Render textured quad
        glActiveTexture(GL_TEXTURE0)

        self.texture.Bind()
        glBindVertexArray(self.__VAO)
        # glViewport(0, 0, self.width, self.height)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        # glViewport(0, 0, self.width, self.height)



# class Foo:
#     def __init__(self, data=None, other=None):
#         if data is not None:
#             self.data = data
#         if other is not None:
#             self.__dict__ = dict(other.__dict__)


