# -*- coding: utf-8 -*-

__author__ = 'jeong-yonghan'

def adaptive_thr(data):
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

    import numpy as np

    mysignal = data
    mymax = {}

    # 우리가 가진 수식들.
    Vpeak = 0
    Fs = 75  # Sampling Frequency
    StdPPG = np.std(mysignal)
    thr_old = 0.5 * np.max(mysignal)
    thr_new = 0
    Sr = -0.6


    # slope = -0.75
    # start = 0.2*max(mysignal)
    adap = [thr_old]
    mode = 'thr'
    cross = False
    adap_it = 0

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
            prev_thr = adap[len(adap) - 2]
            cur_thr = adap[len(adap) - 1]
            prev_sig = mysignal[idx - 1]
            cur_sig = mysignal[idx]
            cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig)
        else:
            pass

        if mode == 'thr':
            if cross == False:
                mode = 'thr'
                thr_new = adap[adap_it] + (Sr * (( Vpeak + StdPPG) / Fs))
                adap_it += 1
                adap.append(thr_new)

            elif cross == True:
                mode = 'sig'
                adap.append(cur_sig)
                adap_it += 1
                continue

        elif mode == 'sig':
            if cur_sig > prev_sig:
                adap.append(cur_sig)
                adap_it += 1
            if cur_sig < prev_sig:
                adap.append(cur_sig)
                adap_it += 1
                mode = 'thr'
                mymax.update({idx: prev_sig})
                Vpeak = prev_sig
                continue
    return [adap, mymax]