# Integration Repo for our Capstone project
## Before using this 
* It is recommended to get to know related repositories in this project
  * Path planning 
  * YOLO-V3 (video_yolo.py is a demo for YOLO)
  * Simulation
* Some modifications are needed according to different environments.
  * YOLO model should be put into it. Models for different applications have been uploaded to our Google drive.(Mujoco, plt, real)
  * The target directory (Mujoco or Jetbot) should be changed 
  * Some constant (like turning angle, Astar ratio) might need to be be changed according to physical measurement 
* The conclusion file in the conclusion folder is recommended to be checked if you are new to this.

# Run the video_real.py file
* It can get pictures from jpg/png or window_capture or camera. 
  * It is recommended to run with window_capture, but you may need a second screen.
  * If you want to use virtual2D file in this directory, run video_real first and then run virtual2D in another terminal. But there might be some error. 
  * If you want to test with the camera, use the third line.
  * All these 3 methods are included in the file. Check them.
* Then YOLO is used for object detection 
* The detected results are used for path planning with algorithms
* The decider will use the result from Path planning and YOLO to send out the command to Jetbot.

# Reinforcement Learning added 
## Before running RL: 
* refer to path planning repo to learn how to train and save the neural network model 
* train the neural network and replace it with DQNnet.pkl

## Run video_RL.py file 
* Before running this, make sure that your DQNnet.pkl is trained for your own environment
* Hopefully, it can be tested well in the real environment 

# Good luck.
* You can contact Zion by email: ziondeng@berkeley.edu
* Go bears!
