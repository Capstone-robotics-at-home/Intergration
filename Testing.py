from JetbotPy import Decider
from Astar import Astar
from Path_Utils import plotting


def Astar_search(objects, decider):
    """ Searching conducting
    :return: path points """
    obstacle_ls = objects['Obstacle']
    s_start = decider.get_position()
    s_goal = objects['Target'][0]
    jetbot_size = objects['Jetbot'][-4:]
    if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
        obstacle_ls = [obstacle_ls]

    astar = Astar(s_start, s_goal, obstacle_ls,jetbot_size)
    # astar = Astar(s_start, s_goal, obstacle_ls)
    path_sol, visited = astar.searching()
    return path_sol


def get_obs_set(obstacle_list, margin_size):
    # the input style: [[(623, 165), 546, 700, 288, 42]], [834, 1073, 636, 287]
    margin_x = (margin_size[1] - margin_size[0]) // 2 
    margin_y = (margin_size[2] - margin_size[3]) // 2 
    if obstacle_list == []:
        raise ValueError('Obstacle list is empty')
    obs = set() 
    for o in obstacle_list:
        left, right, top, bottom = o[-4:]  # the 4 parameters of the obstacle 'box'
        for x in range(left - margin_x, right+1 + margin_x):
            for y in range(bottom - margin_y, top+1 + margin_y):
                obs.add((x,y))

    return obs 


def realtime_search(objects):
    jetbot_pos, jetbot_size = objects['Jetbot'][0], objects['Jetbot'][-4:]
    grab_pos = objects['Grabber'][0]
    decider = Decider(jetbot_pos, grab_pos)

    obstacle_ls = objects['Obstacle']
    s_start = objects['Jetbot'][0]
    s_goal = objects['Target'][0]
    if type(obstacle_ls[0]) == type(()):  # if there is only one obstacle:
        obstacle_ls = [obstacle_ls]
    astar = Astar(s_start, s_goal, obstacle_ls, jetbot_size)
    # astar = Astar(s_start, s_goal, obstacle_ls)
    Original_path, visited = astar.searching()

    plot = plotting.Plotting(s_start, s_goal, obstacle_ls)
    plot.animation(Original_path, visited, 'AStar')

    path = Original_path
    obs_set = get_obs_set(obstacle_ls,jetbot_size)

    while len(path) > decider.Horizon:
        decider.jetbot_step(path, obs_set)
        path = Astar_search(objects, decider)

    trajectory = decider.get_trajectory()
    print('Terminate, Total number of movements is: %d' % len(trajectory))
    plot.plot_traj(Original_path, trajectory)


if __name__ == '__main__':

    objects = {'Jetbot': [(210, 462), 107, 314, 577, 347],
               'Obstacle': [(758, 292), 693, 823, 388, 180],
               'Target': [(1070, 199), 1036, 1105, 256, 143],
               'Grabber': [(174, 591), 141, 207, 660, 523]}

    realtime_search(objects)
