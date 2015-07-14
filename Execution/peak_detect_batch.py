# -*- coding: utf-8 -*-

# Computing Module
import numpy as np
import matplotlib.pyplot as plt


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


def list_difference(mylist):
    return [y-x for y, x in  zip(mylist[1:] , mylist[:-1] )    ]


def adaptive_thr(mysignal, Fs, StdPPG, thr_old, Sr, refract, Vpeak):
    # thr_old 들어가는 인수는 출발값

    mymax = {}

    # 우리가 가진 수식들.
    #Vpeak = 0
    #Fs = 75  # Sampling Frequency
    #StdPPG = np.std(mysignal)
    #thr_old = 0.5 * np.max(mysignal)
    #Sr = -0.3
    cur_loc = 0
    prev_loc = 0
    #refract = 0.6

    adap = {}
    mode = 'thr'
    cross = False


    for idx in range(len(mysignal)):
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
                else:
                    mode = 'sig'
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
    return adap, mymax




def main():
    testnum, orig_mysignal = mydata()
    Fs = 75
    bat_sec = 10
    bat_idx = bat_sec * Fs
    bat_iter = 0
    Sr = -0.3
    refract = 1.0
    starting = 0
    gain_max = {}
    RR_interval = []


    while 1:
        old_break_num = len(gain_max)
        print starting + bat_idx
        print "\n"
        # Batch 신호 정하고, 시작인덱스 잘라내기
        if bat_iter == 0:
            bat_signal = orig_mysignal[:bat_idx]
            print bat_iter, "signal cut!", bat_idx
        else:
            starting = np.max(gain_max.keys()) # Batch Start
            bat_signal = orig_mysignal[int(starting) : starting + bat_idx]
            print "start from", starting, "end at ", starting + bat_idx

        StdPPG = np.std(bat_signal)

        # 시작 고도
        if bat_iter == 0:
            bat_start = 0.5 * np.max(bat_signal)
            Vpeak = 0
        else:
            bat_start = bat_signal[0]
            Vpeak = bat_start

        print str(bat_iter) + "th start amplitude : " + str(bat_start)
        print str(bat_iter) + "th start point idx : " + str(starting)


        adap, mymax =  adaptive_thr(bat_signal, Fs, StdPPG, thr_old=bat_start, Sr=Sr, refract = refract, Vpeak=Vpeak)

        new_mymax = {}
        print bat_iter, " OLD MYMAX : ", mymax
        for key in mymax:
            new_mymax.update( { key + starting : mymax[key]      }  )

        # 1. new_mymax 를 key로 sorting하고
        # 2. sorting된 키의 차이를 저장할것

        locs =  sorted(new_mymax.keys())
        diff_locs = list_difference(locs)

        if bat_iter > 0:
            if len(new_mymax) > 0:
                small_key = np.min( new_mymax.keys()  )
                RR_interval.append(  small_key - starting   )
            else:
                pass

        for idx in diff_locs:
            RR_interval.append(idx)




        print bat_iter, " starting is ",starting
        print bat_iter, " NEW MYMAX : ", new_mymax
        print bat_iter, "RR_interval", RR_interval
        gain_max.update(new_mymax)
        print bat_iter, "Gain MAX", gain_max.keys()

        plt.figure(bat_iter)
        plt.title(str(bat_iter)+"th batch" )
        plt.xlabel("Batch Index")
        plt.ylabel("PPG Modified Voltage")
        plt.plot(bat_signal,'b')
        plt.plot(adap.values(),'g')

        for key in sorted(mymax):
            plt.plot(key, mymax[key], 'ro')

        bat_iter += 1

        new_break_num = len(gain_max)
        if old_break_num == new_break_num:
            break

    print RR_interval
    plt.show()


if __name__ == "__main__":
    main()