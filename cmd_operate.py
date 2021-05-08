'''
 # @ Author: Zion Deng
 # @ Description: write 'cmd.txt' to dir  or read cmd.txt, send command through socket
 '''


import time 
import socket

PATH = '../Capstone_Simulation/cmd.txt'  # remember to change it to the right directory
def cmd_writer(s_cmd): 
    target = open(PATH,'w')
    target.write(s_cmd)
    target.close() 

def cmd_reader():
    cmd_txt = open(PATH,'r')
    cmd = cmd_txt.read()
    cmd_txt.close()

    return cmd


if __name__ == '__main__':
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    DURATION =0.01

    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        try:
            cmd = cmd_reader()
        except:
            continue
        # cmd = np.random.choice(['forward', 'left', 'right'])
        time.sleep(DURATION)
        print('\r',cmd, end='')
        clientsocket.send(bytes(cmd,"utf-8"))

    