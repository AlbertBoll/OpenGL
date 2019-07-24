from OpenGL.GL import *
from breakout.Shader import Shader
import numpy as np
import pyrr
from pyrr.vector3 import length
import glfw
import pygame
from breakout.Texture2D import Texture2D
from enum import Enum
from breakout.SpriteRenderer import SpriteRender
from breakout.GameLevel import GameLevel
from breakout.GameObject import GameObject
from breakout.BallObject import BallObject
from breakout.ParticleGenerator import ParticleGenerator
from breakout.PostProcessor import PostProcessing
from breakout.PowerUp import PowerUp

# all the shader file put in the dict

sprite_shader_dict = {"vs": "shader/sprite.vs.glsl",
                      "fs": "shader/sprite.fs.glsl",
                      "gs": None}

particle_shader_dict = {"vs": "shader/particle.vs.glsl",
                        "fs": "shader/particle.fs.glsl",
                        "gs": None}

post_processing_dict = {"vs": "shader/post_processing.vs.glsl",
                        "fs": "shader/post_processing.fs.glsl",
                        "gs": None}


# dict of PowerUp image file
PowerUp_ImgFile = {"speed": "powerup_image/powerup_speed.png",
                   "sticky": "powerup_image/powerup_sticky.png",
                   "passthrough": "powerup_image/powerup_passthrough.png",
                   "increase": "powerup_image/powerup_increase.png",
                   "confuse": "powerup_image/powerup_confuse.png",
                   "chaos": "powerup_image/powerup_chaos.png"}


# All the CONST
BALL_RADIUS = 12.5
INITIAL_BALL_VELOCITY = pyrr.Vector3([100., -350., 0.])
PLAYER_SIZE = pyrr.Vector3([100., 20., 0.])
PLAYER_VELOCITY = 500.
ShakeTime = 0.0

# global Player, Ball
# Player = GameObject("paddle.png", pos=playerPos, size=PLAYER_SIZE)
# Ball = BallObject("awesomeface.png", pos=ballPos, velocity=INITIAL_BALL_VELOCITY)

# enum type holds the Game's state and collision direction
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class GameState(Enum):
    GAME_ACTIVE = 0
    GAME_MENU = 1
    GAME_WIN = 2
# print(GameState(0))


# All the game functions outside the Game class
def VectorDirection(target):
    compass = [pyrr.Vector3([0., 1., 0.]), pyrr.Vector3([1., 0., 0.]),
               pyrr.Vector3([0., -1., 0.]), pyrr.Vector3([-1., 0., 0.])]
    max_ = 0.
    best_match = -1
    for i in range(4):
        # dot_product = pyrr.vector3.dot(pyrr.vector3.normalise(target), compass[i])
        dot_product = pyrr.vector3.dot(target/(np.linalg.norm(target) + 1e-16), compass[i])
        if dot_product >= max_:
            max_ = dot_product
            best_match = i

    return Direction(best_match)


def clamp(val, lower_bound, upper_bound):
    return pyrr.Vector3([max(lower_bound.x, min(val.x, upper_bound.x)),
                         max(lower_bound.y, min(val.y, upper_bound.y)),
                         0])


def CheckCollision1(object_1, object_2):
    # Check collision between game object and ball object AABB-Circle collision, and return tuple

    center = object_1.pos+pyrr.Vector3([object_1.Radius, object_1.Radius, 0])
    aabb_half_extents = pyrr.Vector3([object_2.size.x/2, object_2.size.y/2, 0])
    aabb_center = object_2.pos + aabb_half_extents
    difference = center - aabb_center
    clamped = clamp(difference, -aabb_half_extents, aabb_half_extents)
    closest = aabb_center + clamped
    difference = closest - center
    # print(length(difference) < object_1.Radius)
    if length(difference) <= object_1.Radius:
        return True, VectorDirection(difference), difference
    # return length(difference) < object_1.Radius
    else:
        return False, Direction.UP, pyrr.Vector3([0., 0., 0.])


def CheckCollision2(GameObject_1, GameObject_2):
    # AABB - AABB collision return boolean
    collisionX = (GameObject_1.pos.x + GameObject_1.size.x >= GameObject_2.pos.x)\
                 and (GameObject_2.pos.x + GameObject_2.size.x >= GameObject_1.pos.x)
    collisionY = (GameObject_1.pos.y + GameObject_1.size.y >= GameObject_2.pos.y)\
                 and (GameObject_2.pos.y + GameObject_2.size.y >= GameObject_1.pos.y)

    return collisionX and collisionY

def ShouldSpawn(chance):
    random = np.random.randint(chance)              # rand() % chance
    return random == 0

def IsOtherPowerUpActive(powerUps, type):
    for powerUp in powerUps:
        if powerUp.Activated:
            if powerUp.Type == type:
                return GL_TRUE
    return GL_FALSE

def PlayBackgroundSound(sound_file, i=-1):
    pygame.mixer.init()
    # pygame_mixer_music to creat background music
    sound1 = pygame.mixer.music
    sound1.load(sound_file)
    sound1.play(i)

def PlaySoundEffect(file):
    # pygame_mixer_sound to play sound effect.
    sound2 = pygame.mixer.Sound(file)
    sound2.play()



# Game holds all game-related state and functionality.
class Game:
    # State = GameState
    Levels = []
    Level = 3

    def __init__(self, width, height, state=GameState.GAME_ACTIVE):
        self.width = width
        self.height = height
        self.state = state
        self.keys = [False] * 1024
        self.PowerUps = []

    def Init(self):
        # create shader
        self.shader = Shader()
        self.shader_ = Shader()
        self.post_processing_shader = Shader()

        # Compile shader
        self.shader.Compile(sprite_shader_dict)
        self.shader_.Compile(particle_shader_dict)
        self.post_processing_shader.Compile(post_processing_dict)
        projection = pyrr.matrix44.create_orthogonal_projection(0, self.width, self.height, 0, -1., 1.)
        self.shader.Use()
        # self.shader_.Use()
        self.shader.SetMatrix4("projection", projection)
        self.shader.SetInteger("sprite", 0)
        self.shader_.Use()
        self.shader_.SetMatrix4("projection", projection)
        self.shader_.SetInteger("sprite", 0)
        self.texture = Texture2D()  # for sprite
        self.texture_ = Texture2D()  # for particle
        self.texture.Generate("gameobject_image/background.jpg")
        self.texture_.Generate("gameobject_image/particle.png")
        # self.texture_back = Texture2D()
        # self.texture_back.Generate("background.jpg")
        self.Renderer = SpriteRender(self.shader)
        self.Particles = ParticleGenerator(self.shader_, self.texture_, 500)
        self.postEffect = PostProcessing(self.post_processing_shader, self.width, self.height)
        # self.postEffect = PostProcessing(self.post_processing_shader, custom_width, custom_height)
        game_level_one = GameLevel()
        game_level_one.Load("tiledata/one.txt", self.width, self.height*0.5)
        game_level_two = GameLevel()
        game_level_two.Load("tiledata/two.txt", self.width, self.height * 0.5)
        game_level_three = GameLevel()
        game_level_three.Load("tiledata/three.txt", self.width, self.height * 0.5)
        game_level_four = GameLevel()
        game_level_four.Load("tiledata/four.txt", self.width, self.height * 0.5)
        self.Levels.append(game_level_one)
        self.Levels.append(game_level_two)
        self.Levels.append(game_level_three)
        self.Levels.append(game_level_four)
        # self.Level = 0
        playerPos = pyrr.Vector3([self.width/2 - PLAYER_SIZE.x/2, self.height-PLAYER_SIZE.y, 0.])
        ballPos = playerPos + pyrr.Vector3([PLAYER_SIZE.x/2-BALL_RADIUS, -2*BALL_RADIUS, 0.])
        # global Player, Ball
        self.Player = GameObject("gameobject_image/paddle.png", pos=playerPos, size=PLAYER_SIZE)
        self.Ball = BallObject("gameobject_image/awesomeface.png", pos=ballPos, velocity=INITIAL_BALL_VELOCITY)
        PlayBackgroundSound("./gamesound/breakout.mp3")  # Play as background music



        # def __del__(self):
    #     del self.Player, self.Ball

    def Update(self, dt):
        global ShakeTime
        self.Ball.Move(dt, self.width)
        self.DoCollision()
        self.Particles.Update(dt, self.Ball, 5, pyrr.Vector3([self.Ball.Radius/2, self.Ball.Radius/2,
                                                              self.Ball.Radius/2]))

        self.UpdatePowerUps(dt)

        if ShakeTime > 0.0:
            ShakeTime -= dt
            if ShakeTime <= 0.0:
                self.postEffect.Shake = GL_FALSE
        if self.Ball.pos.y >= self.height:
            self.ResetLevel()
            self.ResetPlayer()

    def ProcessInput(self, dt):
        if self.state == GameState.GAME_ACTIVE:
            velocity = PLAYER_VELOCITY * dt
            if self.keys[glfw.KEY_A]:
                if self.Player.pos.x >= 0:
                    self.Player.pos.x -= velocity
                    if self.Ball.Stuck:
                        self.Ball.pos.x -= velocity
            if self.keys[glfw.KEY_D]:
                if self.Player.pos.x <= self.width - self.Player.size.x:
                    self.Player.pos.x += velocity
                    if self.Ball.Stuck:
                        self.Ball.pos.x += velocity

            if self.keys[glfw.KEY_SPACE]:
                self.Ball.Stuck = False

    def DoCollision(self):
        global ShakeTime
        for brick in self.Levels[self.Level].Bricks:
            if not brick.destroyed:
                # if CheckCollision(Ball, brick):
                #     if not brick.is_solid:
                #         brick.destroyed = True
                collision = CheckCollision1(self.Ball, brick)
                if collision[0]:  # if collision is True
                    if not brick.is_solid:
                        brick.destroyed = True
                        self.SpawnPowerUps(brick)

                        # play sound effect
                        PlaySoundEffect("./gamesound/bleep_wav1.wav")

                    else:
                        ShakeTime = 0.05
                        self.postEffect.Shake = GL_TRUE

                        # play sound effect
                        PlaySoundEffect("./gamesound/solid.wav")

                    dir = collision[1]
                    diff_vector = collision[2]
                    if not(self.Ball.PassThrough and (not brick.is_solid)):
                        if dir == Direction.LEFT or dir == Direction.RIGHT:
                            # Ball.velocity.x *= -1
                            self.Ball.velocity[0] *= -1
                            penetration = self.Ball.Radius - abs(diff_vector.x)
                            if dir == Direction.LEFT:
                                self.Ball.pos.x += penetration
                            else:
                                self.Ball.pos.x -= penetration

                        else:
                            # Ball.velocity.y = Ball.velocity.y * -1
                            self.Ball.velocity[1] *= -1
                            penetration = self.Ball.Radius - abs(diff_vector.y)
                            if dir == Direction.UP:
                                self.Ball.pos.y -= penetration
                            else:
                                self.Ball.pos.y += penetration

        # Also check collisions on PowerUps and if so, activate them
        for power_up in self.PowerUps:
            if not power_up.destroyed:
                if power_up.pos.y >= self.height:
                    power_up.destroyed = GL_TRUE
                if CheckCollision2(self.Player, power_up):

                    # Collided with player, now activate powerUp
                    self.ActivatePowerUp(power_up)
                    power_up.destroyed = GL_TRUE
                    power_up.Activated = GL_TRUE

                    # play sound effect
                    PlaySoundEffect("./gamesound/powerup.wav")

        # And finally check collisions for player pad (unless stuck)
        result = CheckCollision1(self.Ball, self.Player)
        if not self.Ball.Stuck and result[0]:
            centerBoard = self.Player.pos.x + self.Player.size.x/2
            distance = self.Ball.pos.x+self.Ball.Radius-centerBoard
            percentage = distance/(self.Player.size.x/2)
            strength = 2.0
            oldVelocity = self.Ball.velocity
            # Ball.velocity.x = INITIAL_BALL_VELOCITY.x * percentage * strength
            self.Ball.velocity[0] = INITIAL_BALL_VELOCITY.x * percentage * strength
            # Ball.velocity.y *= -1
            self.Ball.velocity[1] = -1 * abs(self.Ball.velocity[1])
            self.Ball.velocity = pyrr.vector3.normalise(self.Ball.velocity)*pyrr.vector3.length(oldVelocity)
            self.Ball.Stuck = self.Ball.Sticky

            # play sound effect
            PlaySoundEffect("./gamesound/bleep_wav2.wav")

    def Render(self):
        # print(self.Particles.lastUsedParticle)
        if self.state == GameState.GAME_ACTIVE:
            # self.postEffect.texture.Generate_(self.width, self.height, None)

            # Begin rendering to postprocessing quad
            self.postEffect.BeginRender()

            # self.Renderer.initRenderData()

            # Draw background
            self.Renderer.DrawSprite(self.texture, pyrr.Vector3([0., 0., 0]),
                                     pyrr.Vector3([self.width, self.height, 0]), 0., pyrr.Vector3([1., 1., 1.]))
            # self.Renderer.initRenderData()

            # Draw level
            self.Levels[self.Level].Draw(self.Renderer)
            # self.Renderer.initRenderData()

            # Draw player
            self.Player.Draw(self.Renderer)

            # Draw PowerUps
            for powerUp in self.PowerUps:
                if not powerUp.destroyed:
                    powerUp.Draw(self.Renderer)

            # Draw particles
            self.Particles.draw()

            # Draw balls
            self.Ball.Draw(self.Renderer)

            # End rendering to postprocessing quad
            self.postEffect.EndRender()

            # Render postprocessing quad
            self.postEffect.Render(glfw.get_time())

    def ResetLevel(self):

        if self.Level == 0:
            self.Levels[0].Load("tiledata/one.txt", self.width, self.height * 0.5)

        elif self.Level == 1:
            self.Levels[1].Load("tiledata/two.txt", self.width, self.height * 0.5)

        elif self.Level == 2:
            self.Levels[2].Load("tiledata/three.txt", self.width, self.height * 0.5)

        else:
            self.Levels[3].Load("tiledata/four.txt", self.width, self.height * 0.5)

    def ResetPlayer(self):
        del self.Ball, self.Player
        Player_pos = pyrr.Vector3([self.width/2 - PLAYER_SIZE.x/2, self.height-PLAYER_SIZE.y, 0.])
        # Player_size = PLAYER_SIZE

        # self.Player.size = PLAYER_SIZE
        # self.Player.pos = pyrr.Vector3([self.width/2 - PLAYER_SIZE.x/2, self.height-PLAYER_SIZE.y, 0.])
        # self.Ball.Reset(self.Player.pos+pyrr.Vector3([PLAYER_SIZE.x/2-BALL_RADIUS, -2*BALL_RADIUS, 0]),
        #                 INITIAL_BALL_VELOCITY)
        self.Player = GameObject("paddle.png", pos=Player_pos, size=PLAYER_SIZE)
        self.Ball = BallObject("awesomeface.png",
                               pos=self.Player.pos+pyrr.Vector3([PLAYER_SIZE.x/2-BALL_RADIUS, -2*BALL_RADIUS, 0]),
                               velocity=INITIAL_BALL_VELOCITY)

    def SpawnPowerUps(self, block):
        # if chance is 1/45
        if ShouldSpawn(45):
            color = pyrr.Vector3([0.5, 0.5, 1.0])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["speed"], "speed", 0., GL_FALSE, block.pos, color))

        if ShouldSpawn(45):
            color = pyrr.Vector3([1.0, 0.5, 1.0])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["sticky"], "sticky", 20., GL_FALSE, block.pos, color))

        if ShouldSpawn(45):
            color = pyrr.Vector3([0.5, 1.0, 0.5])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["passthrough"], "pass-through", 10., GL_FALSE, block.pos, color))

        if ShouldSpawn(45):
            color = pyrr.Vector3([1., 0.6, 0.4])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["increase"], "pad-size-increase", 0., GL_FALSE, block.pos, color))

        if ShouldSpawn(15):  # if chance is 1/15
            color = pyrr.Vector3([1.0, 0.3, 0.3])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["confuse"], "confuse", 15., GL_FALSE, block.pos, color))

        if ShouldSpawn(15):
            color = pyrr.Vector3([0.9, 0.25, 0.25])  # color tuple of PowerUp
            self.PowerUps.append(PowerUp(PowerUp_ImgFile["chaos"], "chaos", 15., GL_FALSE, block.pos, color))

    def ActivatePowerUp(self, powerUp):

        # check the powerUp type
        if powerUp.Type == "speed":
            self.Ball.velocity *= 1.2

        elif powerUp.Type == "sticky":
            self.Ball.Sticky = GL_TRUE
            self.Player.color = pyrr.Vector3([1.0, 0.5, 1.0])

        elif powerUp.Type == "pass-through":
            self.Ball.PassThrough = GL_TRUE
            self.Player.color = pyrr.Vector3([1.0, 0.5, 0.5])

        elif powerUp.Type == "pad-size-increase":
            self.Player.size.x += 50

        elif powerUp.Type == "confuse":
            if not self.postEffect.Chaos:
                self.postEffect.Confuse = GL_TRUE  # Only activate if chaos wasn't already active

        else:
            if not self.postEffect.Confuse:
                self.postEffect.Chaos = GL_TRUE

    def UpdatePowerUps(self, dt):
        for powerUp in self.PowerUps:
            powerUp.pos += powerUp.velocity * dt
            if powerUp.Activated:
                powerUp.Duration -= dt
                if powerUp.Duration <= 0:
                    powerUp.Activated = GL_FALSE
                    if powerUp.Type == "sticky":
                        if not IsOtherPowerUpActive(self.PowerUps, "sticky"):
                            self.Ball.Sticky = GL_FALSE
                            self.Player.color = pyrr.Vector3([1., 1., 1.])
                    elif powerUp.Type == "pass-through":
                        if not IsOtherPowerUpActive(self.PowerUps, "pass-through"):
                            self.Ball.PassThrough = GL_FALSE
                            self.Ball.color = pyrr.Vector3([1., 1., 1.])

                    elif powerUp.Type == "confuse":
                        if not IsOtherPowerUpActive(self.PowerUps, "confuse"):
                            self.postEffect.Confuse = GL_FALSE

                    elif powerUp.Type == "chaos":
                        if not IsOtherPowerUpActive(self.PowerUps, "chaos"):
                            self.postEffect.Chaos = GL_FALSE

        return [i for i in self.PowerUps if (not i.destroyed or not i.Activated)]  # list comprehension
        # return list(filter(lambda x: not x.destroyed or not x.Activated, self.PowerUps)) # filter function














