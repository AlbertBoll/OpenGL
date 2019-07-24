from OpenGL.GL import *
from PIL import Image
import numpy
import os

class Texture2D:
    def __init__(self, Wrap_S=GL_REPEAT, Wrap_T=GL_REPEAT, Filter_Min=GL_LINEAR, Filter_Max=GL_LINEAR):
        self.Wrap_S = Wrap_S
        self.Wrap_T = Wrap_T
        self.Filter_Min = Filter_Min
        self.Filter_Max = Filter_Max
        self.ID = glGenTextures(1)

    def Generate(self, file):
        glBindTexture(GL_TEXTURE_2D, self.ID)
        image = Image.open(file)
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
        #img_data = numpy.array(list(image.getdata()), numpy.uint8)
        if image.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        elif image.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, image.width, image.height, 0, GL_RED, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.Wrap_S)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.Wrap_T)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.Filter_Min)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.Filter_Max)
        # glBindTexture(GL_TEXTURE_2D, 0)

    def Generate_(self, width, height, data):
        # self.Width = width
        # self.Height = height
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.Wrap_S)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.Wrap_T)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.Filter_Min)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.Filter_Max)
        glBindTexture(GL_TEXTURE_2D, 0)

    def Bind(self):
        glBindTexture(GL_TEXTURE_2D, self.ID)

    def Clear(self):
        glDeleteTextures(self.ID)


