def writer(cmd):
    target_file = open('../Capstone_Simulation/gym_rev/cmd.txt','w')
    target_file.write(cmd)
    target_file.close() 

if __name__ == '__main__':
    
    while True:
        c = input('input a command line: ')
        writer(c) 