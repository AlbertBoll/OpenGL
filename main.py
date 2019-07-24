from breakout.Game import Game

# from breakout.Shader import Shader
# from breakout.Texture2D import Texture2D
# from breakout.PostProcessor import PostProcessing
# from breakout.Game import post_processing_dict
import pyrr
from OpenGL.GL import *
import glfw


BALL_RADIUS = 12.5
PLAYER_SIZE = pyrr.Vector3([100., 20., 0.])
w_width, w_height = 1980, 1200

# Breakout = Game(w_width, w_height)
Breakout = Game(w_width, w_height)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if (key >= 0) and (key < 1024):
        if action == glfw.PRESS:
            Breakout.keys[key] = True
        elif action == glfw.RELEASE:
            Breakout.keys[key] = False

def window_resize(window, width, height):
    # global w_width, w_height
    glViewport(0, 0, width, height)
    Breakout.width = width
    Breakout.height = height

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(w_width, w_height, "Breakout", None, None)
    # window = glfw.create_window(new_width, new_height, "Breakout", None, None)
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    # glfw.set_window_size_callback(window, window_resize)
    glfw.set_framebuffer_size_callback(window, window_resize)
    # glGetError()
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    Breakout.Init()
    deltaTime = 0.
    lastFrame = glfw.get_time()
    # Breakout.state = Breakout.State.GAME_ACTIVE
    # Breakout.state = Breakout.State.GAME_ACTIVE

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        # print(current_frame)
        deltaTime = current_frame - lastFrame
        lastFrame = current_frame
        glfw.poll_events()

        # Breakout.postEffect.Init(Breakout.width, Breakout.height)
        # print(Breakout.width, Breakout.height)
        # Breakout.postEffect = PostProcessing(shader, Breakout.width, Breakout.height)
        Breakout.ProcessInput(deltaTime)
        Breakout.Update(deltaTime)
        glClearColor(0., 0., 0., 1.)
        glClear(GL_COLOR_BUFFER_BIT)
        # glViewport(0, 0, new_width, new_height)
        Breakout.Render()
        glfw.swap_buffers(window)
    glfw.terminate()

main()