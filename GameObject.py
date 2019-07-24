import pyrr
from breakout.Texture2D import Texture2D

# from breakout.SpriteRenderer import SpriteRender
Position = pyrr.Vector3([0., 0., 0.])
Size = pyrr.Vector3([1., 1., 0.])
Velocity = pyrr.Vector3([0., 0., 0.])
# Color = pyrr.Vector3([0.5, 0.5, 0.5])
Color = pyrr.Vector3([1.0, 1.0, 1.0])
# Sprite = Texture2D()
Rotation = 0.
IsSolid = False
Destroyed = False

class GameObject:
    def __init__(self, img_file, pos=Position, size=Size, color=Color, velocity=Velocity, rotation=Rotation,
                 is_solid=IsSolid, destroyed=Destroyed):
        self.sprite = Texture2D()
        self.Upload(img_file)
        self.pos = pos
        self.size = size
        self.color = color
        self.velocity = velocity
        self.is_solid = is_solid
        self.destroyed = destroyed
        self.rotation = rotation

    def Upload(self, img_file):
        self.sprite.Generate(img_file)

    def Draw(self, renderer):

        renderer.DrawSprite(self.sprite, self.pos, self.size, self.rotation, self.color)






