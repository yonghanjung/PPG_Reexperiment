# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

# Computing Module
import numpy as np
import matplotlib.pyplot as plt


def main():
    _, mysignal = mydata()
    Fs = 75
    sec = 3
    see = 15
    train_sig = mysignal[:Fs * sec]

    next_few = mysignal[Fs * sec:]
    #next_few = mysignal[Fs * sec: Fs * see * sec]

    adap, mymax, mycross = adaptive_thr(train_sig)

    thres_consider = mycross.values() + mymax.values()
    thres_consider.pop(0)
    stdPPG = np.std(thres_consider)

    down_thres = np.mean( thres_consider )
    prev = adap[len(adap)-2]
    cur = adap[len(adap)-1]
    window_size = 30
    window = train_sig[len(train_sig)-1 - window_size: len(train_sig)-1]

    plt.figure(0)

    plt.plot(train_sig,'b')
    plt.plot(adap.values(),'g')

    for key in mycross:
        plt.plot(key,  mycross[key], 'ro')
    for key in mymax:
        plt.plot(key,  mymax[key], 'ko')

    plt.plot( Fs*sec -1  , prev,'bo')
    plt.plot( Fs*sec   , cur ,'bo')
    plt.plot([down_thres] * len(train_sig),'r--')

    plt.figure(1)
    plt.plot(next_few,'b')

    refraction = 0
    my_new_max = {}


    for idx in range(len(next_few)):
        window.pop(0)
        window.append(next_few[idx])
        next = next_few[idx]
        #next = sum(list_difference(window))

        print idx, prev, cur, next, down_thres, saddle(prev,cur,next)

        if saddle(prev,cur,next) == "peak":
            if next > down_thres:
                if len(my_new_max.keys()) > 0:
                    if idx - np.max(my_new_max.keys()) > refraction * Fs :
                        prev_key = np.max(my_new_max.keys())
                        my_new_max.update( {idx-1 : cur  } )
                        cur_key = np.max(my_new_max.keys())

                        down_thres = down_thres + ((my_new_max[cur_key] - my_new_max[prev_key]) / Fs)

                else :
                    my_new_max.update( {idx : cur  } )

        prev = cur
        cur = next
        #plt.plot(idx, down_thres,'r.')


    RR_locs = []
    for key in my_new_max:
        RR_locs.append(float(key) / float(Fs))
    RR_locs = sorted(RR_locs)
    print ""
    print "RR_location", RR_locs
    print "RR_interval", list_difference(RR_locs)

    plt.plot( range(len(next_few))  , [down_thres] * len(next_few) ,'r--')

    for key in my_new_max:
        plt.plot(key,my_new_max[key],'ro')

    plt.show()

# adap의 마지막바로 전
# adap의 마지막
# 새로운 포인트 하나


def list_difference(mylist):
    return [y-x for y, x in  zip(mylist[1:] , mylist[:-1] )    ]



def saddle(prev,cur,next):
    # prev는 Thres의 마지막 포인트
    # cur은 들어오는 신호
    # next는 바로 다음에 들어오는 신호
    if prev < cur:
        if next <= cur:
            return "peak"
        else:
            return "inc"
    else:
        return "dec"




def conv(a,b):
    lena = len(a)
    lenb = len(b)
    length = lena + lenb - 1

    a = a + [0] * (length-lena)
    b = b + [0] * (length - lenb)

    y = [0] * length

    for myiter in range(length):
        mysum = 0
        for idx in range(myiter+1):
            mysum += a[idx] * b[myiter - idx]
        y[myiter] = mysum
    return y








# DATA IMPORT
def mydata():
    from Module.data_call import data_call
    from Module.bandpass import butter_bandpass_filter

    testnum = 0
    mysignal = data_call("PPG_KW_long", testnum, 0)

    #mysignal = butter_bandpass_filter(mysignal,0.125,10,1000)
    return testnum, mysignal


def check_cross(prev_thr, prev_sig, cur_thr, cur_sig):
    if prev_thr > prev_sig:
        if cur_thr < cur_sig:
            return True
            # 크로스포인트는 과거와 현재 사이에 찍힌다.
            # 즉, 현재포인트부터 신호를 받는게 좋다.
        else:  # cur_thr > cur_sig
            return False
    else:
        return False


def adaptive_thr(mysignal):
    mymax = {}

    # 우리가 가진 수식들.
    Vpeak = 0
    Fs = 75  # Sampling Frequency
    StdPPG = np.std(mysignal)
    thr_old = 0.5 * np.max(mysignal)
    thr_new = 0
    Sr = -0.3
    cur_loc = 0
    prev_loc = 0
    refract = 0.6

    # slope = -0.75
    # start = 0.2*max(mysignal)
    adap = {}
    mode = 'thr'
    cross = False
    mycross = {}

    for idx in range(len(mysignal)):
        # MODE CHECK
        if idx > 0:
            prev_thr = adap[idx-1]
            cur_thr = adap[idx-1]+ (Sr * (( Vpeak + StdPPG) / Fs))
            prev_sig = mysignal[idx - 1]
            cur_sig = mysignal[idx]
            cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig)
        else:
            pass

        if mode == 'thr':
            if cross == False:
                mode = 'thr'
                if idx == 0:
                    thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs))
                else:
                    thr_new = adap[idx-1] + (Sr * (( Vpeak + StdPPG) / Fs))
                #adap_it += 1
                #adap.append(thr_new)
                adap.update( {idx :thr_new }  )

            elif cross == True:
                if prev_loc != 0:
                    if idx - prev_loc < refract * Fs:
                        mode = 'thr'
                    else:
                        mode = 'sig'
                        mycross.update ( {idx : thr_new   }   )
                else:
                    mode = 'sig'
                    mycross.update ( {idx : thr_new   }   )
                adap.update( {idx : cur_sig}  )
                #adap.append(cur_sig)
                #adap_it += 1
                continue

        elif mode == 'sig':
            if cur_sig >= prev_sig:
                adap.update({idx : cur_sig})

            else:
                prev_loc = cur_loc
                cur_loc = idx-1
                new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs))
                adap.update({idx : new_thr} )

                mode = 'thr'
                mymax.update({idx-1: prev_sig})
                Vpeak = prev_sig
                continue
    return adap, mymax, mycross





if __name__ == "__main__":
    main()
