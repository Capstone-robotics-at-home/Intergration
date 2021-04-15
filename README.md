# Integration Repo for our Capstone project
## Before using this 
* It is recommended to get to know previous work in this project
  * Path planning 
  * YOLO-V3 (video_yolo.py is a demo for YOLO)
  * Simulation
* Some modifications are needed 
  * YOLO model should be put into it 
  * The target directory (Mujoco or Jetbot) should be changed 
  * Some constant like turnning angle should be changed according to physical measurement 

# Run the video_real.py file
* It can get picture from jpg/png or window_capture or camera. 
  * It is recommended to run with window_capture, but you may need a second screen.
  * If you want to use virtual2D file in this directory, run video_real first and then run virtual2D in another terminal. But there might be some error. 
  * If you want to test with camera, use the third line.
  * All these 3 method are included in the file. Check them.
* Then YOLO is used for object detection 
* The detected results are used for path planning with algorithms(A* now RL in the future(maybe)) 
* The decider will use the result from Path planning and YOLO to send out the command to Jetbot.

# Reinforcement Learning added 
## Before running RL: 
* refer to path planning repo to learn how to train and save the neural network model 
* train the neural network and replace it with DQNnet.pkl

## Run video_RL.py file 
* It is not working so well now.
* Hopefully it can be tested well in real environment 
* Good luck.

