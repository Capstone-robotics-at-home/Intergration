#-------------------------------------#
# Use screen recoder to monitor Mujoco 
#-------------------------------------#
import os,sys 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/YOLOv3")
from yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
from Astar import Astar
from Path_Utils import plotting, env
from Testing import get_obs_set, Astar_search
from JetbotPy import Decider
from screen_recorder import window_capture 


yolo = YOLO()
# get the camera 
# capture=cv2.VideoCapture("1.mp4" Or 0)
# capture=cv2.VideoCapture("YOLOv3/img/b.mp4") 
# capture=cv2.VideoCapture(1) 

decider = Decider(True)
fps = 0.0
PathEnable = True
while(True):
    t1 = time.time()
    # get one frame
    frame = window_capture()  
    # # change format，BGRtoRGB
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # # change to Image
    frame = Image.fromarray(np.uint8(frame))

    # start detecting 
    frame, objects = yolo.detect_image(frame)

    if not decider.obj_isvalid(objects):  # if the detected objects are not valid -> recheck 
        print('\r','Detection invalid', end = ' ')
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
        astar = Astar(s_start, s_goal, obstacle_ls,jetbot_size)
        path, visited = astar.searching()

        plot = plotting.Plotting(s_start, s_goal, obstacle_ls)
        frame = plot.plot_image_path(frame,path,decider.Horizon)

        ## let the Mojoco_jetbot move 

        decider.reinit(s_start, s_goal)
        obs_set = get_obs_set(obstacle_ls,jetbot_size)

        if len(path) > decider.Horizon:
            decider.jetbot_step(path,obs_set)
            

    frame = np.array(frame)

    # # RGBtoBGR to satisfy opencv display format 
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    fps  = ( fps + (1./(time.time()-t1)) ) / 2
    frame = cv2.putText(frame, "fps= %.2f"%(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cmd_txt = open(decider.target_path,'r')
    cmd = cmd_txt.read(10)
    frame = cv2.putText(frame, cmd, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    print("fps= %.2f"%(fps),' || command is: ', cmd)

    cv2.imshow("video",frame)


    c= cv2.waitKey(30) & 0xff 
    if c==27:
        capture.release()
        break
