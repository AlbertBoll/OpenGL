import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *


def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return str.encode(shader_source)

class Shader:
    # def __init__(self, ID):
    #     self.ID = ID

    def Use(self):
        glUseProgram(self.ID)

    def Compile(self, shader_dict):
        vert_shader = load_shader(shader_dict["vs"])
        frag_shader = load_shader(shader_dict["fs"])
        # compile vertex shader
        shaderV = compileShader([vert_shader], GL_VERTEX_SHADER)
        # compiler fragment shader
        shaderF = compileShader([frag_shader], GL_FRAGMENT_SHADER)

        if shader_dict["gs"] is not None:
            global shaderG
            # compile Geometry shader
            geo_shader = load_shader(shader_dict["gs"])
            shaderG = compileShader([geo_shader], GL_GEOMETRY_SHADER)

        program = glCreateProgram()
        if not program:
            raise RuntimeError('glCreateProgram faled!')

        # attach shaders
        glAttachShader(program, shaderV)
        glAttachShader(program, shaderF)
        if shader_dict["gs"] is not None:
            glAttachShader(program, shaderG)

        glLinkProgram(program)

        # Check the link status
        linked = glGetProgramiv(program, GL_LINK_STATUS)
        if not linked:
            infoLen = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
            infoLog = ""
            if infoLen > 1:
                infoLog = glGetProgramInfoLog(program, infoLen, None)
            glDeleteProgram(program)
            raise RuntimeError("Error linking program:\n%s\n", infoLog)

        self.ID = program

        # Delete the shaders as they're linked into our program now and no longer exist
        glDeleteShader(shaderV)
        glDeleteShader(shaderF)
        if shader_dict["gs"] is not None:
            glDeleteShader(shaderG)

    def Setfloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def SetInteger(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def SetVector2f(self, name, vec2):
        glUniform2f(glGetUniformLocation(self.ID, name), vec2.x, vec2.y)

    def SetVector3f(self, name, vec3):
        glUniform3f(glGetUniformLocation(self.ID, name), vec3.x, vec3.y, vec3.z)

    def SetVector4f(self, name, vec4):
        glUniform4f(glGetUniformLocation(self.ID, name), vec4.x, vec4.y, vec4.z, vec4.w)

    def SetMatrix4(self, name, matrix):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, matrix)

    def _CheckCompileErrors(self, object, type):
        if type != "PROGRAM":
            success = glGetShaderiv(object, GL_COMPILE_STATUS)
            if not success:
                infoLog = glGetShaderInfoLog(object, 1024, None)
                print("| ERROR::SHADER: Compile-time error: Type: {}\n{}\n".format(type, infoLog))
                print("-------------------------------------------")
        else:
            success = glGetProgramiv(object, GL_LINK_STATUS)
            if not success:
                infoLog = glGetProgramiv(object, 1024, None)
                print("| ERROR::Shader: Link-time error: Type: {}\n{}\n".format(type, infoLog))
                print("-------------------------------------------")

    def Clear(self):
        glDeleteProgram(self.ID)


