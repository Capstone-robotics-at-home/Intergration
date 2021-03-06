from JetbotPy import Jetbot
from Astar import Astar
from Path_Utils import plotting  

def Astar_search(objects, jetbot):
    """ Searching conducting
    :return: path points """
    obstacle_ls = objects['Obstacle']
    s_start = jetbot.get_position() 
    s_goal = objects['Target'][0] 
    if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
        obstacle_ls = [obstacle_ls]

    astar = Astar(s_start, s_goal, obstacle_ls)
    path_sol, visited = astar.searching()
    return path_sol 

def get_obs_set(obstacle_list):
    if obstacle_list == []:
        raise ValueError('Obstacle list is empty')
    obs = set() 
    for o in obstacle_list:
        left, right, top, bottom = o[-4:]  # the 4 parameters of the obstacle 'box'
        for x in range(left, right+1):
            for y in range(bottom, top+1):
                obs.add((x,y))

    return obs 

# objects = {'Jetbot': [(95, 46), 83, 107, 63, 28], 
#     'Obstacle': [(110, 30), 100,120,80,0], 
#     'Target': [(134, 17), 130, 137, 24, 9], 
#     'Grabber': [(105, 62), 100, 110, 72, 52]}

objects =  {'Jetbot': [(210, 462), 107, 314, 577, 347], 
                    'Obstacle': [(758, 292), 693, 823, 388, 197], 
                    'Target': [(1070, 199), 1036, 1105, 256, 143], 
                    'Grabber': [(174, 591), 141, 207, 660, 523]}

jetbot_pos = objects['Jetbot'][0]
grab_pos = objects['Grabber'][0]
bot = Jetbot(jetbot_pos,grab_pos)

obstacle_ls = objects['Obstacle']
s_start = objects['Jetbot'][0]
s_goal = objects['Target'][0] 
if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
    obstacle_ls = [obstacle_ls]
astar = Astar(s_start, s_goal, obstacle_ls)
Original_path, visited = astar.searching()

plot = plotting.Plotting(s_start, s_goal, obstacle_ls)
plot.animation(Original_path,visited,'AStar')

path = Original_path
obs_set = get_obs_set(obstacle_ls)

while len(path) > 15:
    bot.jetbot_step(path,obs_set)
    path = Astar_search(objects, bot) 

print('Terminate')
trajectory = bot.get_trajectory()
# print(trajectory)


