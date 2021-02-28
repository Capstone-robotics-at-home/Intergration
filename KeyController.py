from pynput.keyboard import Key,Listener
from JetbotPy import Jetbot


class Control():
    def __init__(self):
        self.dir_ = None #  Make dir as member param. Or it won't be changed in on_press.
        self.isCtrling = True
        print('Press ↑ to st art')

    def getdir(self):
        self.dir_ = None    # if it is not right, return None
        def on_press(key):
            if key == Key.up:self.dir_ = 1
            elif key == Key.down:self.dir_ = 4
            elif key == Key.left:self.dir_ = 2
            elif key == Key.right:self.dir_ = 3
            return False
        listener = Listener(on_press=on_press) # create listener 
        listener.start()    # start listening, press a button
        listener.join()     # join thread 
        listener.stop()     # finish thread 
        return self.dir_ 


if __name__ == '__main__':
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
    