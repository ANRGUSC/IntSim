# Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved.
#     Contributor: Angela Zhang
#     Read license file in main directory for more details  


import random
import csv
import time
t=time.time()

p = 0.5 # 0.1 to 0.9
N = 5#5 10 50 100
Tsim=3000 #fixed
x=0
jam_count=0
percentage =0
r=0.5
Ncount=0
Wcount=0
#initialize lists
ATI = '0'
EWBI =['0']*N #0 or 'w'
SNBI =['0']*N #0 or 'n'
EWAI =['0']*N
SNAI =['0']*N
timesteps=['']*51

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
    global r
    global Wcount
    global Ncount
    currentATI=ATI
    lShift(EWAI)
    uShift(SNAI)
    a = random.uniform(0, 1)
    #print ("a",a)
    if EWBI[0] == '0' and SNBI[0] == 'N':
        ATI = uShift(SNBI)
        lShift(EWBI)
        Ncount -=1
    elif EWBI[0] == 'W' and SNBI[0] == '0':
        ATI = lShift(EWBI)
        uShift(SNBI)
        Wcount -= 1
    elif EWBI[0]=='W' and SNBI[0] == 'N':
        #prioritize N
        if Ncount>Wcount:
            for index in range(N - 1):
                if EWBI[index]== '0':
                    EWBI[index]=EWBI[index+1]
                    EWBI[index + 1] = '0'
            ATI = uShift(SNBI)
            Ncount -= 1
        #prioritize W
        elif Wcount > Ncount:
            for index in range(N - 1):
                if SNBI[index] == '0':
                    SNBI[index] = SNBI[index + 1]
                    SNBI[index + 1] = '0'
            ATI = lShift(EWBI)
            Wcount -= 1
        elif Wcount == Ncount: #randomselect if Ncount=Wcount
            # let W pass
            if a < r:
                for index in range(N - 1):
                    if SNBI[index] == '0':
                        SNBI[index] = SNBI[index + 1]
                        SNBI[index + 1] = '0'
                ATI = lShift(EWBI)
                Wcount -= 1
            # let N pass
            if a > r:
                for index in range(N - 1):
                    if EWBI[index] == '0':
                        EWBI[index] = EWBI[index + 1]
                        EWBI[index + 1] = '0'
                ATI = uShift(SNBI)
                Ncount -= 1
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

data = open('PrioritizeCrowdedRd.csv','w')
header = ["n","p","jam count","%"]

with data:
    writer = csv.writer(data)
    writer.writerow(header)

for n in range(5, 105, 5):
    print('n: ', n)
    for p in frange(0.1, 0.91, 0.01):
        #print('p: ', p)
        jam_count = 0
        timesteps = [''] * 51
        for trial in range(1, 51):
            ATI = '0'
            EWBI = ['0'] * N  # 0 or 'w'
            SNBI = ['0'] * N  # 0 or 'n'
            EWAI = ['0'] * N
            SNAI = ['0'] * N
            #print('trial: ', trial)
            for T in range(0, Tsim):
                updateTraffic()
                x = random.uniform(0, 1)
                #print('p =', x)
                if x < p:
                    if EWBI[N - 1] == 'W':
                        jam_count += 1
                        if T > 1:
                            timesteps[jam_count - 1] = T
                        else:
                            timesteps[jam_count - 1] = ' '
                        break
                        #print('EW: traffic jam')
                    else:
                        EWBI[N - 1] = 'W'  # N-1 is last element in list
                        Wcount +=1
                        #print('car added to EW road')
                else:
                    #print('car not added to EW road')
                    pass

                y = random.uniform(0, 1)
                #print('p =', y)
                if y < p:
                    if SNBI[N - 1] == 'N':
                        #print('SN: traffic jam')
                        jam_count += 1
                        if T > 1:
                            timesteps[jam_count - 1] = T
                        else:
                            timesteps[jam_count - 1] = ' '
                        break
                    else:
                        SNBI[N - 1] = 'N'  # N-1 is last element in list
                        Ncount +=1
                        #print('car added to SN road')
                else:
                    #print('car not added to SN road')
                    pass
        # print('jam count:', jam_count)
        percentage = jam_count / trial * 100
        # print('%:', percentage)
        tempdata = [n, p, jam_count, percentage]
        data = open('PrioritizeCrowdedRd.csv', 'a')
        with data:
            writer = csv.writer(data)
            writer.writerow(tempdata+timesteps)


elaspsed=time.time()-t
print('time:', elaspsed)
