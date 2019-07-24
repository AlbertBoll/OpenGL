import numpy as np
import pyrr
from breakout.GameObject import GameObject

class GameLevel:
    Bricks = []

    def Load(self, file, levelWidth, levelHeight):
        self.Bricks.clear()
        # tileData = []
        tileData = list(np.loadtxt(file).astype(np.uint8))
        # tileData.append(data)
        if len(tileData) > 0:
            self.Init(tileData, levelWidth, levelHeight)

    def Draw(self, renderer):
        for tile in self.Bricks:
            if not tile.destroyed:
                # renderer.initRenderData()
                tile.Draw(renderer)

    def IsCompleted(self):
        for tile in self.Bricks:
            if (not tile.is_solid) and (not tile.destroyed):
                return False
        return True

    def Init(self, tileData, levelWidth, levelHeight):
        height = len(tileData)
        width = len(tileData[0])
        unit_width, unit_height = levelWidth/width, levelHeight/height
        for y in range(height):
            for x in range(width):
                # pos = pyrr.Vector3([unit_width * x, unit_height * y, 0.])
                # size = pyrr.Vector3([unit_width, unit_height, 0.])
                if tileData[y][x] == 1:  # solid tile
                    pos = pyrr.Vector3([unit_width * x, unit_height * y, 0.])
                    size = pyrr.Vector3([unit_width, unit_height, 0.])
                    color = pyrr.Vector3([0.8, 0.8, 0.7])
                    obj = GameObject("gameobject_image/block_solid.png", pos, size, color)
                    obj.is_solid = True
                    self.Bricks.append(obj)
                elif tileData[y][x] > 1:
                    color = pyrr.Vector3([1., 1., 1.])
                    if tileData[y][x] == 2:
                        color = pyrr.Vector3([0.2, 0.6, 1.0])
                    elif tileData[y][x] == 3:
                        color = pyrr.Vector3([0.0, 0.7, 0.0])
                    elif tileData[y][x] == 4:
                        color = pyrr.Vector3([0.8, 0.8, 0.4])
                    elif tileData[y][x] == 5:
                        color = pyrr.Vector3([1., 0.5, 0.])
                    pos = pyrr.Vector3([unit_width * x, unit_height * y, 0.])
                    size = pyrr.Vector3([unit_width, unit_height, 0.])
                    obj = GameObject("gameobject_image/block.png", pos, size, color)
                    self.Bricks.append(obj)




