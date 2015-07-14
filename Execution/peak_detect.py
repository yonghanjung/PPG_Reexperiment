# -*- coding: utf-8 -*-

'''
그래프 짜는거 새로짜기
'''


def main():
    def mydata():
        from Module.data_call import data_call
        from Module.bandpass import butter_bandpass_filter

        testnum = 1
        mysignal = data_call("PPG_KW_long", testnum, 0)
        mysignal = mysignal

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


    def adaptive_thr():
        import numpy as np

        testnum, mysignal = mydata()
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


        for idx in range(len(mysignal)):

            # 모드 : sig, thr
            # thr 모드 : 직선을 타고 내려간다.
            # sig 모드 : 신호를 타고 올라간다.

            # 알고리즘
            # 시작은 thr모드
            # 기울기0, 스타트0 으로 직선을 그린다.
            # 교차인지 확인
            # 만일 교차가 아니라면 계속 thr모드로 진행
            # 교차면 sig모드 변환
            # 다음 iteration
            # sig모드이면
            # increasing 이면 타고 올라간다.
            # decreasing 이면 thr 모드 변환
            # 현재의 신호 포인트를 맥스로 저장
            # slope은 그대로
            # start는 맥스
            # 새로운 x를 잡아서 진행한다.
            # 다음 iteration

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

    def plotting():
        import matplotlib.pyplot as plt

        adap, mymax = adaptive_thr()
        testnum, mysignal = mydata()
        Len = len(mysignal)

        # for idx, key in sorted(enumerate(mymax)):
        #     plt.plot(key , mymax[key], 'ro')

        plt.plot(mysignal, 'b')

        plt.plot(adap.values() , 'g')
        plt.grid(True)
        # plt.xticks([i/float(75) for i in range(0,Len)])
        plt.xlabel("X index (1 data point every 1/75 sec.)")
        plt.ylabel("Scale modified Voltage value")
        plt.title("#" + str(testnum) + " Samples from Kiwook")

        plt.show()

    A,B = adaptive_thr()
    print B
    plotting()


if __name__ == "__main__":
    main()