# Integration Repo for our Capstone project
## Before using this 
* It is recommended to get to know previous work
  * Path planning 
  * YOLO-V3 (video_yolo.py is a demo for YOLO)
* Some modifications are needed 
  * YOLO model should be put into it 
  * The target directory (Mujoco or Jetbot) should be changed 
  * Some constant like turnning angle should be changed according to physical measurement 

## JetbotPy is a file for Jetbot class 
* The decider class is designed as the dicision brain for Jetbot.
* Since the movement of the real jetbot is not accurate, we also used inaccurate motions for calculation
* It can send command (left/right/forward) in .txt format to desired folder.

## Run the video_mujoco.py file
* It can get picture from window_capture or camera 
* Then YOLO is used for object detection 
* The detected results are used for path planning with algorithms(A* now RL in the future(maybe)) 
* The decider will use the result from Path planning and YOLO to send out the command to Jetbot.

## Run the Tesing.py file. 
* The position of the jetbot can be calculated 
* The trajectory of the jetbot including position and heading can be printed and plotted 

