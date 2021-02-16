from JetbotPy import Jetbot
from KeyController import Control

bot = Jetbot() 
c = Control() 
c.isCtrling = True  

while c.isCtrling:
    # OR you can directly change the cmd here by 1,2,3,4,,,
    cmd = c.getdir()
    if cmd == 1: bot.forward()
    elif cmd == 2: bot.left()
    elif cmd == 3: bot.right()
    elif cmd == 4: bot.back()
    else:
        print('Wrong number, Lost Control')
        c.isCtrling = False