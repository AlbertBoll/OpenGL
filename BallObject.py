from breakout.GameObject import GameObject

import pyrr

class BallObject(GameObject):
    # Radius = 12
    # Stuck = True
    def __init__(self, image, pos, velocity, radius=12., stuck=True, sticky=False, pass_through=False):
        super().__init__(image, pos, velocity=velocity, size=pyrr.Vector3([2*radius, 2*radius, 0]),
                         color=pyrr.Vector3([1., 1., 1.]))
        self.Radius = radius
        self.Stuck = stuck
        self.velocity = velocity
        self.Sticky = sticky
        self.PassThrough = pass_through

    def Move(self, dt, window_width):
        if not self.Stuck:
            self.pos += self.velocity*dt
            if self.pos.x <= 0.:
                self.velocity[0] *= -1
                self.pos.x = 0

            elif self.pos.x >= window_width-self.size.x:
                self.velocity[0] *= -1
                self.pos.x = window_width-self.size.x

            if self.pos.y <= 0.:
                self.velocity[1] *= -1
                self.pos.y = 0.
        return self.pos

    def Reset(self, position, velocity):
        self.pos = position
        self.velocity = velocity
        self.Stuck = True
        self.PassThrough = False
        self.Sticky = False




