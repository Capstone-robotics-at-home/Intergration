'''
 # @ Author: Zion Deng
 # @ Description: Simulation env build on plt
 '''

from matplotlib import pyplot as plt
import numpy as np 
from matplotlib import patches as mpatches
from cmath import pi, sin, cos

DT = 0.01  # the fresh time 
V = 0.6  # velocity 
V_THETA = 2*pi / 0.7  # angular velocity 

class JetbotPlt():
    """ calculate and record state of the Jetbot in simulation env  """
    def __init__(self):
        self.V = 0.6  # velocity
        self.V_THETA = 2*pi / 0.7  # angular velocity
        self.GRABBER_LEN = 0.15 # distance from center of body to grabber
        self.theta = 0.0 # initial angle 
        self.x = 0.0 # initial position of body in x coordinate 
        self.y = 0.0 # initial position of body in y coordinate

    def left(self):
        self.theta += DT * self.V_THETA 
        if self.theta > 2*pi:
            self.theta -= 2*pi
        self.render_cart()

    def right(self):
        self.theta -= DT * self.V_THETA
        if self.theta < -2 *pi: 
            self.theta += 2 *pi
        self.render_cart()

    def forward(self):
        dl = DT * self.V 
        dx, dy = dl *cos(self.theta), dl *sin(self.theta)
        self.x += dx 
        self.y += dy
        self.render_cart()

    def render_cart(self):
        body_center = np.array([self.x, self.y])
        grabber_dx = self.GRABBER_LEN * cos(self.theta)
        grabber_dy = self.GRABBER_LEN* sin(self.theta)
        grabber_center = body_center + np.array([grabber_dx, grabber_dy])
        # body
        body = mpatches.Circle(body_center, 0.1, color = 'b')
        ax.add_patch(body)
        # grabber 
        grabber = mpatches.RegularPolygon(grabber_center,6, 0.05, color = 'g')
        ax.add_patch(grabber)
        linex = [body_center[0], grabber_center[0]]
        liney = [body_center[1], grabber_center[1]]
        plt.plot(linex,liney, color = 'g')

    def act(self, cmd):
        """ act according to command """
        if cmd == 'forward':
            self.forward() 
        elif cmd == 'left':
            self.left()
        elif cmd == 'right':
            self.right()
        elif cmd == '0':
            self.render_cart()
        else: 
            print('Unknown command')
        

def canvas_init():
    """ draw obstacles and target """
    plt.cla()
    plt.axis('equal')
    # plt.autoscale(False)
    plt.plot([0,0,2,2,0], [0,1,1,0,0], color = 'b', alpha = 0.001)  # draw boundary
    # obstacles 
    obstacle = mpatches.Rectangle(obs_center, 0.4,0.2, color = 'y')
    ax.add_patch(obstacle)
    # target
    target = mpatches.RegularPolygon(target_center,3,0.1, color = 'r')
    ax.add_patch(target)
    plt.axis('off')


plt.ion()
jetbot = JetbotPlt() # Jetbot class
fig, ax = plt.subplots() 
obs_center = np.array([0.5,0.0])
target_center = np.array([1.2,1.0])

def simulation2D():
    i = 0 
    # cmd_file = open('cmd.txt', 'w')
    # cmd_file.write('0')  # initiate the command with '0'
    # cmd_file.close()

    while True:
        canvas_init()
        # action = np.random.choice(['forward','left','right'])
        cmd_txt = open('cmd.txt','r')
        cmd = cmd_txt.read()
        cmd_txt.close()
        jetbot.act(cmd)
        plt.pause(DT)
        plt.savefig('pic.jpg')
        i += 1

if __name__ == '__main__':
    simulation2D()