'''
 # @ Author: Zion Deng
 # @ Description: Real time integration with YOLO, Reinforcement Learning
 '''
import os,sys 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/YOLOv3")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/Path_Utils")

from matplotlib import pyplot as plt
from RLmodel_test import DQNnet
from Path_Utils.simple_RL_env import CartEnv
from Path_Utils.simple_RL_run import Net

from YOLOv3.yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
from Astar import Astar
from Path_Utils import plotting, env
from Testing import get_obs_set, Astar_search
from JetbotPy import Decider
from frame_capturer import window_capture 

def change_cmd2str(cmd):
    '''
    action 0: forward
    action 1: left
    action 2: right
    but the real action is the mirror of the virtual environment
    '''        
    if cmd == 0:
        return 'forward'
    elif cmd == 1: 
        return 'right'
    elif cmd == 2:
        return 'left'
    else: 
        print('ERROR!')
        return '0'


def RL_search(objects):
    """ Path finding methods with Reinforcement Learning 
    return: the recorded commands to the goal, solved trajectory"""   

    # generate env
    obstacle_ls = objects['Obstacle']
    s_start = objects['Jetbot'][0]
    s_goal = objects['Target'][0]
    if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
        obstacle_ls = [obstacle_ls]
    env = CartEnv(s_start, s_goal, obstacle_ls) 

    # initialize RL brain
    dqn = DQNnet('DQNnet.pkl') 
    info = 0  # initialize info with 0 means nothing happened

    # try until find solution
    while info is not 1: 
        s = env.reset(objects['Jetbot'][0],objects['Grabber'][0])
        ep_r = 0 
        step = 0 
        # while info is not 1: 
        while True:
            step += 1 
            a = dqn.choose_action(s)                 
            s_,r,done,info = env.step(a) 

            ep_r += r 
            if done: 
                print('\rEpisode information number: ', info,end ='')
                if info == 1:
                    print('\n================================ Path Found =================================')
                    trajectory = env.decider.get_trajectory()
                    trajectory_ls = [(visit[0],visit[1]) for visit in trajectory]
                    return env.decider.cmd_record[0], trajectory_ls[::-1]
                break
            s = s_
    if info is not 1:
        print('================================ERROR: path not found================================')
        return [0], [()]
    
    return [],[()]

if __name__ == '__main__':
    yolo = YOLO()
    # get the camera 
    # capture=cv2.VideoCapture("1.mp4" Or 0)
    # capture=cv2.VideoCapture("YOLOv3/img/b.mp4") 
    # capture=cv2.VideoCapture(1) 

    decider = Decider(if_write = False)  # use it to send command only 

    fps = 0.0
    PathEnable = True
    Ratio = 1.5  # The extended boundary param

    while(True):
        t1 = time.time()
        # get one frame
        frame = window_capture() 
        # ref,frame=capture.read()  # if you are using camera to get frame, use this line and also uncomment the line above with respect to capture.
        # # change format，BGRtoRGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # # change to Image
        frame = Image.fromarray(np.uint8(frame))

        # start detecting 
        frame, objects = yolo.detect_image(frame)

        if not decider.obj_isvalid(objects):  # if the detected objects are not valid -> recheck 
            print('\r','Detection invalid', end = ' ')
            decider.cmd = '0'
            decider.send_cmd()
            PathEnable = False
        else: 
            PathEnable = True 

        # Use Astar
        if PathEnable:
            s_start = objects['Jetbot'][0]
            s_goal = objects['Target'][0]
            obstacle_ls = objects['Obstacle']
            if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
                obstacle_ls = [obstacle_ls]
            jetbot_size = objects['Jetbot'][-4:] 

            sol, trj = RL_search(objects) 
            decider.cmd = change_cmd2str(sol)
            decider.send_cmd()
            plot = plotting.Plotting(s_start, s_goal, obstacle_ls)
            frame = plot.plot_image_path(frame,trj,decider.Horizon)


        frame = np.array(frame)

        # # RGBtoBGR to satisfy opencv display format 
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        frame = cv2.putText(frame, "fps= %.2f"%(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cmd = decider.cmd
        frame = cv2.putText(frame, cmd, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print("fps= %.2f"%(fps),' || command is: ', cmd)

        cv2.imshow("video",frame)


        c= cv2.waitKey(30) & 0xff 
        if c==27:
            # capture.release()
            break
