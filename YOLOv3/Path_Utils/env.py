import numpy as np 

class Env:
    def __init__(self, obstacles, margin_size = [0,0,0,0]):
        self.x_range = 51  # size of the background 
        self.y_range = 31 
        # self.motions = [(2,0),(-2,0),(0,2),(0,-2),
        #                 (1,1),(1,-1),(-1,1),(-1,-1)]
        self.motions = 20 * np.array(
            [(5,0),(-5,0),(0,5),(0,-5),
            (3,4),(3,-4),(-3,4),(-3,4),                   
            (4,3),(4,-3),(-4,3),(-3,4),]
        )


        self.obs = self.obs_map_mod(obstacles, margin_size)

    def update_obs(self, obs):
        self.obs = obs

    def obs_map_mod(self, obs_ls, margin_size = [0,0,0,0]):
        ''' modify the map by the detected obstacles
        :return: map of obstacles  '''

        # the input style: [[(623, 165), 546, 700, 288, 42]], [834, 1073, 636, 287]
        margin_x = (margin_size[1] - margin_size[0]) // 2 
        margin_y = (margin_size[2] - margin_size[3]) // 2 
        if obs_ls == []:
            raise ValueError('Obstacle list is empty')
        obs = set() 
        for o in obs_ls:
            left, right, top, bottom = o[-4:]  # the 4 parameters of the obstacle 'box'
            for x in range(left - margin_x, right+1 + margin_x):
                for y in range(bottom - margin_y, top+1 + margin_y):
                    obs.add((x,y))

        return obs 

    def obs_map(self):
        """  
        Initialize the obstacles' positions
        return: map of obstacles 
        """
        x = self.x_range 
        y = self.y_range 
        obs = set()

        # margins 
        for i in range(x):
            obs.add((i,0))
        for i in range(x):
            obs.add((i,y-1))

        for i in range(y):
            obs.add((0,i))
        for i in range(y):
            obs.add((x-1,i))

        # walls 
        for i in range(10, 21):
            obs.add((i, 15))
        for i in range(15):
            obs.add((20, i))

        for i in range(15, 30):
            obs.add((30, i))
        for i in range(16):
            obs.add((40, i))

        return obs 




        
