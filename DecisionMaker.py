# A decision maker for Jetbot while moving 
# The object detection obtained from YOLO should be looking like this: 
# {'Jetbot': [(953, 461), 834, 1073, 636, 287], 
#   'Obstacle': [(623, 165), 546, 700, 288, 42], 
#   'Target': [(1342, 170), 1308, 1377, 249, 92], 
#   'Grabber': [(1054, 626), 1003, 1106, 728, 525]}
import math 

pi = 3.1415926

def checkHeading(objs):
    ''' check where the jetbot is heading for
    :return: the theta of heading angle '''

    pHead = objs['Target'][0] 
    pBody = objs['Jetbot'][0] 
    x1, y1 = pHead[0], pHead[1] 
    x2, y2 = pBody[0], pBody[1] 
    dx, dy = x1-x2, y1-y2 
    if dx > 0:  # first quadrant and forth quadrant 
        return math.atan((y1-y2)/(x1-x2))
    if dx < 0 and dy > 0:  # second quadrant 
        return math.atan((y1-y2)/(x1-x2)) + pi  
    if dx < 0 and dy < 0:  # third quadrant 
        return math.atan((y1-y2)/(x1-x2)) - pi 
 

if __name__ == '__main__':
    objects = {'Jetbot': [(953, 461), 834, 1073, 636, 287], 
            'Obstacle': [(623, 165), 546, 700, 288, 42], 
            'Target': [(1342, 170), 1308, 1377, 249, 92], 
            'Grabber': [(1054, 626), 1003, 1106, 728, 525]}

    print(checkHeading(objects) * 360 / (2 * pi)) 

    

