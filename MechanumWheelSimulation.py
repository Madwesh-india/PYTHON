import numpy as np
import pyglet
from pyglet.window import Window
from pyglet import shapes, gl

# Configuration

#Smaller size of the screen is considered to be 
room = 100. #meter

# obtained/updated from the window
roomWidth = 0. #meter
roomHeight = 0. #meter

windowWidth = 0. #px
windowHeight = 0. #px

"""
The width of the bot is measured between center of the wheels
The height of the bot is measured between the wheel shafts
"""
botWidth = 0.46 #meter
botHeight = 0.54 #meter
botRadius = 0.072 #meter
botMaxRotationalSpeed = 0.1047198*370 #rad/sec <- 0.1047198*RPM


class Bot:
    def __init__(self, W, H, Radius, MaxRad_S, InitialX=0., InitialY=0., InitialAng=0.):
        self.W = W
        self.H = H
        self.Radius = Radius
        self.MaxRad_S = MaxRad_S
        
        halfW = W/2
        halfH = H/2
        
        self.x = InitialX
        self.y = InitialY
        self.theta = InitialAng

        self.W1 = 0.
        self.W2 = 0.
        self.W3 = 0.
        self.W4 = 0.
        
        self.BotVel_bot_coordinate = 0.
        self.BotVel_global_coordinate = 0.
        
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
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
    
    def draw(self, batch):
        x, y = toCenter(self.x, self.y)
        w, h = room_to_pix(self.W, self.H)

        rect = shapes.Rectangle(x, y, w, h, color=(255, 22, 20), batch=batch)
        rect.anchor_position = self.x, self.y
        rect.rotation = self.theta
        return rect

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
        self.BotVel_global_coordinate = self.R(self.theta).T@self.BotVel_bot_coordinate
        
        self.x += dt*self.BotVel_global_coordinate[0][0]
        self.y += dt*self.BotVel_global_coordinate[1][0]
        self.theta += dt*self.BotVel_global_coordinate[2][0]

# modifing the window

class Simulator(Window):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)

        global windowWidth, windowHeight, roomWidth, roomHeight
        
        windowWidth = self.width
        windowHeight = self.height

        if windowWidth<windowHeight:
            roomWidth=room
            roomHeight=room*(windowHeight/windowWidth)
        else:
            roomHeight=room
            roomWidth=room*(windowWidth/windowHeight)

        self.bot = Bot(botWidth, botHeight, botRadius, botMaxRotationalSpeed)
        self.bot.setWheelVel(10, 10, 10, 10)

        pyglet.clock.schedule_interval(self.bot.update, 1/120.0)
        self.batch = pyglet.graphics.Batch()



    def on_draw(self):
        self.clear()
        rect = self.bot.draw(self.batch)
        self.batch.draw()

# Converts value from center coordinate frame to left bottom coordinate frame
def toCenter(x, y):
    x, y = room_to_pix(x, y)
    return x+windowWidth/2, y+windowHeight/2

def room_to_pix(width, height):
    return windowWidth*width/roomWidth, windowHeight*height/roomHeight

if __name__ == '__main__':
    config = gl.Config(double_buffer=True)
    window = Simulator(fullscreen=True, config=config)
    pyglet.app.run()