import numpy as np
import pyglet
from pyglet.window import Window

# Configuration

roonWidth = 10 #meter
roonHeight = 10 #meter

windowWidth = 500 #px
windowHeight = 500 #px

"""
The width of the bot is measured between center of the wheels
The height of the bot is measured between the wheel shafts
"""
botWidth = 0.46 #meter
botHeight = 0.54 #meter
botRadius = 0.072 #meter
botMaxRotationalSpeed = 0.1047198*370 #rad/sec <- 0.1047198*RPM


class Bot:
    def __init__(self, W, H, Radius, MaxRad_S, InitialX=0, InitialY=0, InitialAng=0):
        self.W = W
        self.H = H
        self.Radius = Radius
        self.MaxRad_S = MaxRad_S
        
        halfW = W/2
        halfH = H/2
        
        self.x = InitialX
        self.y = InitialY
        self.theta = InitialAng
        
        self.BotVel_bot_coordinate = 0
        self.BotVel_global_coordinate = 0
        
        self.forwardKinamatics = np.array([
            [1, 1, 1, 1],
            [-1, 1, -1, 1],
            [-1/(halfH+halfW), -1/(halfH+halfW), 1/(halfH+halfW), 1/(halfH+halfW)],
        ])/4
        
#         self.inverceKinamatics = np.array([
#             [1, -1, -(halfH+halfW)],
#             [1, 1, -(halfH+halfW)],
#             [1, -1, (halfH+halfW)],
#             [1, 1, (halfH+halfW)]
#         ])
        
        self.R = lambda theta: np.array([
            [cos(theta), sin(theta), 0],
            [-sin(theta), cos(theta), 0],
            [0, 0, 1]
        ])
    
    def setWheelVel(self, W1, W2, W3, W4):
        self.W1 = W1
        self.W2 = W2
        self.W3 = W3
        self.W4 = W4
        
    def update(self, dt):
        wheelVel = self.Radius*np.array([
                                    [self.W1],
                                    [self.W2],
                                    [self.W3],
                                    [self.W4],
                                ])
        
        self.BotVel_bot_coordinate = self.forwardKinamatics@wheelVel
        self.BotVel_global_coordinate = self.R(self.theta)@self.BotVel_bot_coordinate
        
        self.x += dt*self.BotVel_global_coordinate[0][0]
        self.y += dt*self.BotVel_global_coordinate[1][0]
        self.theta += dt*self.BotVel_global_coordinate[2][0]
    
bot = Bot(botWidth, botHeight, botRadius, botMaxRotationalSpeed)

# modifing the window

class Simulator(Window):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.label = pyglet.text.Label('Hello, world!')

    def on_draw(self):
        self.clear()
        self.label.draw()

if __name__ == '__main__':
    window = Simulator()
    pyglet.app.run()