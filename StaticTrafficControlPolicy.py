# Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved.
#     Contributor: Angela Zhang
#     Read license file in main directory for more details  


import random
import csv
import time
t=time.time()

p = 0.1 # 0.1 to 0.9
N = 5 #5 10 50 100
Tsim = 3000 #fixed
jam_count=0
percentage =0

#initialize lists
ATI = '0'
EWBI =['0']*N #0 or 'w'
SNBI =['0']*N #0 or 'n'
EWAI =['0']*N
SNAI =['0']*N
timesteps =['']*101

def lShift(traffic):
    #global ATI
    firstWCar=traffic.pop(0)
    #print(ATI)
    traffic.append('0')
    return firstWCar

def uShift(traffic):
    #global ATI
    firstNCar = traffic.pop(0)
    #print(ATI)
    traffic.append('0')
    return firstNCar

def updateTraffic():
    global SNBI
    global EWBI
    global ATI
    global SNAI
    global EWAI
    currentATI=ATI
    lShift(EWAI)
    uShift(SNAI)
    if EWBI[0] == '0' and SNBI[0] == 'N':
        ATI = uShift(SNBI)
        lShift(EWBI)
    elif EWBI[0]=='W' and SNBI[0] == 'N':
        for index in range (N-1):
            if SNBI[index]== '0':
                SNBI[index]=SNBI[index+1]
                SNBI[index + 1] = '0'
        ATI = lShift(EWBI)
    else:
        ATI = lShift(EWBI)
        uShift(SNBI)
    if currentATI == 'W':
        EWAI[N - 1] = currentATI
    else:
        SNAI[N - 1] = currentATI

def frange(start, end, step):
    tmp = start
    while(tmp < end):
        yield tmp
        tmp += step

data = open('AlwaysWpass.csv','w')
header = ["n","p","jam count","%"]

with data:
    writer = csv.writer(data)
    writer.writerow(header)

for n in range (5,105,5):
   print ('n: ', n)
   for p in frange (0.1,0.91,0.01):
        #print('p: ', p);
        jam_count = 0
        timesteps=['']*101
        for trial in range(1, 101):
            ATI = '0'
            EWBI = ['0'] * N  # 0 or 'w'
            SNBI = ['0'] * N  # 0 or 'n'
            EWAI = ['0'] * N
            SNAI = ['0'] * N
            #print('trial: ', trial);
            # run one trial Tsim=1000 times
            for T in range(1, Tsim + 1):
                #print('step:', T)
                updateTraffic()
                x = random.uniform(0, 1)
                # print ('p =', x)
                if x < p:
                    if EWBI[N - 1] == 'W':
                        #print('*****EW: traffic jam*****')
                        jam_count += 1
                        if T > 1:
                            timesteps[jam_count - 1] = T
                        else:
                            timesteps[jam_count - 1] = ' '
                        #print("timestep:", T)
                        break
                    else:
                        EWBI[N - 1] = 'W'  # N-1 is last element in list
                        # print ('car added to EW road')
                else:
                    pass
                    # print ('car not added to EW road')
                y = random.uniform(0, 1)
                # print('p =', y)
                if y < p:
                    if SNBI[N - 1] == 'N':
                        #print('*******SN: traffic jam********')
                        jam_count += 1
                        if T > 1:
                            timesteps[jam_count - 1] = T
                        else:
                            timesteps[jam_count - 1] = ' '
                        #print("timestep:", T)
                        break
                    else:
                        SNBI[N - 1] = 'N'  # N-1 is last element in list
                        # print('car added to SN road')
                else:
                    pass
        #print('jam count:', jam_count)
        percentage = jam_count / trial * 100
        #print('%:', percentage)
        tempdata = ([n, p, jam_count, percentage])
        data = open('AlwaysWpass.csv', 'a')
        with data:
            writer = csv.writer(data)
            writer.writerow(tempdata+timesteps)

#print('probability:',p)
#print('N roads:',N)
#print('trials:',trial)
elaspsed=time.time()-t
print('time:',elaspsed)
