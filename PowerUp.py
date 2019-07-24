from breakout.GameObject import GameObject
import pyrr

SIZE = pyrr.Vector3([60, 20, 0])
VELOCITY = pyrr.Vector3([0.0, 150.0, 0])

# define Power up class, it inherits the base class GameObject which shares all public member of methods
class PowerUp(GameObject):
    def __init__(self, image, type_, duration, activated, position, color):
        super().__init__(image, position, SIZE, color, velocity=VELOCITY)
        self.Type = type_
        self.Duration = duration
        self.Activated = activated









