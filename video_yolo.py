#-------------------------------------#
#       调用摄像头检测
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

yolo = YOLO()
# get the camera 
# capture=cv2.VideoCapture("1.mp4" Or 0)
capture=cv2.VideoCapture("YOLOv3/img/b.mp4") 
# capture=cv2.VideoCapture(1) 

decider = Decider() 
fps = 0.0
PathEnable = True
while(True):
    t1 = time.time()
    # get one frame
    ref,frame=capture.read()
    # change format，BGRtoRGB
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # change to Image
    frame = Image.fromarray(np.uint8(frame))

    # start detecting 
    frame, objects = yolo.detect_image(frame)

    if not decider.obj_isvalid(objects):  # if all the objects are not detected -> recheck 
        print('\r','Detection invalid.', end = ' ')
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

    frame = np.array(frame)

    # RGBtoBGR to satisfy opencv display format 
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    fps  = ( fps + (1./(time.time()-t1)) ) / 2
    print("fps= %.2f"%(fps), end = ' ')
    # frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("video",frame)


    c= cv2.waitKey(30) & 0xff 
    if c==27:
        capture.release()
        break
