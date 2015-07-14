# -*- coding: utf-8 -*-

# Computing Module
import numpy as np
import matplotlib.pyplot as plt


# DATA IMPORT
class AdaptiveThreshold:
    def __init__(self, Array_SignalinWindow, Flt_SamplingRate ):
        self.Array_PPGinWindow = np.squeeze(np.asarray(Array_SignalinWindow))
        self.Flt_SamplingRate = Flt_SamplingRate

    def check_cross(self, prev_thr, prev_sig, cur_thr, cur_sig):
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

    def adaptive_thr(self):
        # thr_old 들어가는 인수는 출발값
        Dict_MaxLoc_MaxAmp = dict()
        Dict_Loc_ThresholdAmp = dict()
        Flt_NewThreshold = 0.0
        Flt_OldThreshold = np.max(self.Array_PPGinWindow) * 0.5
        Flt_StdPPG = np.std(self.Array_PPGinWindow)
        Flt_VPeak = 0.0
        Flt_SlopeThreshold = -0.3
        Flt_BackThreshold = 0.4 * self.Flt_SamplingRate # Not too much signal
        Flt_CurrSigAmp = 0.0
        Flt_PrevSigAmp = 0.0

        Int_PrevLoc = 0
        Int_CurrLoc = 0

        Bool_ThresholdUpdateMode = True # False : FindingPeak Mode, True : Update Threshold
        Bool_SignalCrossThreshold = False # True if Signal Cross Threshold

        for IntIdx in range(len(self.Array_PPGinWindow)):
            if IntIdx == 0:
                pass
            elif IntIdx > 0:
                Flt_PrevThreshold = Dict_Loc_ThresholdAmp[IntIdx-1]
                Flt_CurrThreshold = Flt_PrevThreshold * (Flt_SlopeThreshold * ((Flt_VPeak + Flt_StdPPG) / self.Flt_SamplingRate))
                Flt_PrevSigAmp = self.Array_PPGinWindow[IntIdx-1]
                Flt_CurrSigAmp = self.Array_PPGinWindow[IntIdx]
                Bool_SignalCrossThreshold = self.check_cross(prev_thr=Flt_PrevThreshold, prev_sig=Flt_PrevSigAmp, cur_thr=Flt_CurrThreshold, cur_sig = Flt_CurrSigAmp)


            # Initial Start
            if Bool_ThresholdUpdateMode == True:
                if Bool_SignalCrossThreshold == False:
                    # Initial Start
                    if IntIdx == 0:
                        Flt_NewThreshold = Flt_OldThreshold + (Flt_SlopeThreshold * (( Flt_VPeak + Flt_StdPPG) / self.Flt_SamplingRate))

                    # Threshold update
                    elif IntIdx > 0:
                        Flt_NewThreshold = Dict_Loc_ThresholdAmp[IntIdx-1] + (Flt_SlopeThreshold * (( Flt_VPeak + Flt_StdPPG) / self.Flt_SamplingRate))
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_NewThreshold


                elif Bool_SignalCrossThreshold == True:
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_CurrSigAmp
                    # If No Previosu Peak existed, and Signal Cross
                    # Then Mode change to find the peak
                    if Int_PrevLoc == 0:
                        Bool_ThresholdUpdateMode = False

                    # If Previous Peak exists
                    elif Int_PrevLoc != 0:
                        if IntIdx - Int_PrevLoc < Flt_BackThreshold:
                            Bool_ThresholdUpdateMode = True
                        elif IntIdx - Int_PrevLoc > Flt_BackThreshold:
                            Bool_ThresholdUpdateMode = False
                    continue

            elif Bool_ThresholdUpdateMode == False:
                # Peak Finding Mode
                if Flt_CurrSigAmp >= Flt_PrevSigAmp:
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_CurrSigAmp
                elif Flt_CurrSigAmp < Flt_PrevSigAmp:
                    Int_PrevLoc = Int_CurrLoc
                    Int_CurrLoc = IntIdx - 1
                    Flt_NewThreshold = Flt_PrevSigAmp * (Flt_SlopeThreshold * ((Flt_VPeak + Flt_StdPPG)/self.Flt_SamplingRate))
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_NewThreshold

                    Bool_ThresholdUpdateMode = True
                    Dict_MaxLoc_MaxAmp[Int_CurrLoc] = Flt_PrevSigAmp
                    Flt_VPeak = Flt_PrevSigAmp
                    continue
        return Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp

#
#
#
#
#
#
#         # 우리가 가진 수식들.
#         #Vpeak = 0
#         #Fs = 75  # Sampling Frequency
#         #StdPPG = np.std(mysignal)
#         #thr_old = 0.5 * np.max(mysignal)
#         #Sr = -0.3
#         cur_loc = 0
#         prev_loc = 0
#         #refract = 0.6
#
#         adap = {}
#         mode = 'thr'
#         cross = False
#
#         if Bool_ThresholdUpdateMode == True:
#             if Bool_SignalCrossThreshold == False:
#                 mode = 'thr'
#                 if idx == 0:
#                     thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs))
#                 else:
#                     thr_new = adap[idx-1] + (Sr * (( Vpeak + StdPPG) / Fs))
#                 #adap_it += 1
#                 #adap.append(thr_new)
#                 adap.update( {idx :thr_new }  )
#
#             elif Bool_SignalCrossThreshold == True:
#                 if prev_loc != 0:
#                     if idx - prev_loc < refract * Fs:
#                         mode = 'thr'
#                     else:
#                         mode = 'sig'
#                 else:
#                     mode = 'sig'
#                 adap.update( {idx : cur_sig}  )
#                 #adap.append(cur_sig)
#                 #adap_it += 1
#                 continue
#
#
#
#
#         for idx in range(len(self.Array_PPGinWindow)):
#             if idx > 0:
#                 prev_thr = adap[idx-1]
#                 cur_thr = adap[idx-1]+ (Sr * (( Vpeak + StdPPG) / Fs))
#                 prev_sig = mysignal[idx - 1]
#                 cur_sig = mysignal[idx]
#                 cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig)
#             else:
#                 pass
#
#             if mode == 'thr':
#                 if cross == False:
#                     mode = 'thr'
#                     if idx == 0:
#                         thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs))
#                     else:
#                         thr_new = adap[idx-1] + (Sr * (( Vpeak + StdPPG) / Fs))
#                     #adap_it += 1
#                     #adap.append(thr_new)
#                     adap.update( {idx :thr_new }  )
#
#                 elif cross == True:
#                     if prev_loc != 0:
#                         if idx - prev_loc < refract * Fs:
#                             mode = 'thr'
#                         else:
#                             mode = 'sig'
#                     else:
#                         mode = 'sig'
#                     adap.update( {idx : cur_sig}  )
#                     #adap.append(cur_sig)
#                     #adap_it += 1
#                     continue
#
#             elif mode == 'sig':
#                 if cur_sig >= prev_sig:
#                     adap.update({idx : cur_sig})
#
#                 else:
#                     prev_loc = cur_loc
#                     cur_loc = idx-1
#                     new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs))
#                     adap.update({idx : new_thr} )
#
#                     mode = 'thr'
#                     mymax.update({idx-1: prev_sig})
#                     Vpeak = prev_sig
#                     continue
#         return adap, mymax
#
#
#
#
#
#
# def mydata():
#     from Module.data_call import data_call
#     from Module.bandpass import butter_bandpass_filter
#
#     testnum = 0
#     mysignal = data_call("PPG_KW_long", testnum, 0)
#
#     #mysignal = butter_bandpass_filter(mysignal,0.125,10,1000)
#     return testnum, mysignal
#
#
# def check_cross(prev_thr, prev_sig, cur_thr, cur_sig):
#     if prev_thr > prev_sig:
#         if cur_thr < cur_sig:
#             return True
#             # 크로스포인트는 과거와 현재 사이에 찍힌다.
#             # 즉, 현재포인트부터 신호를 받는게 좋다.
#         else:  # cur_thr > cur_sig
#             return False
#     else:
#         return False
#
#
# def list_difference(mylist):
#     return [y-x for y, x in  zip(mylist[1:] , mylist[:-1] )    ]
#
#
# def adaptive_thr(mysignal, Fs, StdPPG, thr_old, Sr, refract, Vpeak):
#     # thr_old 들어가는 인수는 출발값
#
#     mymax = {}
#
#     # 우리가 가진 수식들.
#     #Vpeak = 0
#     #Fs = 75  # Sampling Frequency
#     #StdPPG = np.std(mysignal)
#     #thr_old = 0.5 * np.max(mysignal)
#     #Sr = -0.3
#     cur_loc = 0
#     prev_loc = 0
#     #refract = 0.6
#
#     adap = {}
#     mode = 'thr'
#     cross = False
#
#
#     for idx in range(len(mysignal)):
#         if idx > 0:
#             prev_thr = adap[idx-1]
#             cur_thr = adap[idx-1]+ (Sr * (( Vpeak + StdPPG) / Fs))
#             prev_sig = mysignal[idx - 1]
#             cur_sig = mysignal[idx]
#             cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig)
#         else:
#             pass
#
#         if mode == 'thr':
#             if cross == False:
#                 mode = 'thr'
#                 if idx == 0:
#                     thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs))
#                 else:
#                     thr_new = adap[idx-1] + (Sr * (( Vpeak + StdPPG) / Fs))
#                 #adap_it += 1
#                 #adap.append(thr_new)
#                 adap.update( {idx :thr_new }  )
#
#             elif cross == True:
#                 if prev_loc != 0:
#                     if idx - prev_loc < refract * Fs:
#                         mode = 'thr'
#                     else:
#                         mode = 'sig'
#                 else:
#                     mode = 'sig'
#                 adap.update( {idx : cur_sig}  )
#                 #adap.append(cur_sig)
#                 #adap_it += 1
#                 continue
#
#         elif mode == 'sig':
#             if cur_sig >= prev_sig:
#                 adap.update({idx : cur_sig})
#
#             else:
#                 prev_loc = cur_loc
#                 cur_loc = idx-1
#                 new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs))
#                 adap.update({idx : new_thr} )
#
#                 mode = 'thr'
#                 mymax.update({idx-1: prev_sig})
#                 Vpeak = prev_sig
#                 continue
#     return adap, mymax
#
#
#
#
# def main():
#     testnum, orig_mysignal = mydata()
#     Fs = 75
#     bat_sec = 10
#     bat_idx = bat_sec * Fs
#     bat_iter = 0
#     Sr = -0.3
#     refract = 1.0
#     starting = 0
#     gain_max = {}
#     RR_interval = []
#
#
#     while 1:
#         old_break_num = len(gain_max)
#         print starting + bat_idx
#         print "\n"
#         # Batch 신호 정하고, 시작인덱스 잘라내기
#         if bat_iter == 0:
#             bat_signal = orig_mysignal[:bat_idx]
#             print bat_iter, "signal cut!", bat_idx
#         else:
#             starting = np.max(gain_max.keys()) # Batch Start
#             bat_signal = orig_mysignal[int(starting) : starting + bat_idx]
#             print "start from", starting, "end at ", starting + bat_idx
#
#         StdPPG = np.std(bat_signal)
#
#         # 시작 고도
#         if bat_iter == 0:
#             bat_start = 0.5 * np.max(bat_signal)
#             Vpeak = 0
#         else:
#             bat_start = bat_signal[0]
#             Vpeak = bat_start
#
#         print str(bat_iter) + "th start amplitude : " + str(bat_start)
#         print str(bat_iter) + "th start point idx : " + str(starting)
#
#
#         adap, mymax =  adaptive_thr(bat_signal, Fs, StdPPG, thr_old=bat_start, Sr=Sr, refract = refract, Vpeak=Vpeak)
#
#         new_mymax = {}
#         print bat_iter, " OLD MYMAX : ", mymax
#         for key in mymax:
#             new_mymax.update( { key + starting : mymax[key]      }  )
#
#         # 1. new_mymax 를 key로 sorting하고
#         # 2. sorting된 키의 차이를 저장할것
#
#         locs =  sorted(new_mymax.keys())
#         diff_locs = list_difference(locs)
#
#         if bat_iter > 0:
#             if len(new_mymax) > 0:
#                 small_key = np.min( new_mymax.keys()  )
#                 RR_interval.append(  small_key - starting   )
#             else:
#                 pass
#
#         for idx in diff_locs:
#             RR_interval.append(idx)
#
#
#
#
#         print bat_iter, " starting is ",starting
#         print bat_iter, " NEW MYMAX : ", new_mymax
#         print bat_iter, "RR_interval", RR_interval
#         gain_max.update(new_mymax)
#         print bat_iter, "Gain MAX", gain_max.keys()
#
#         plt.figure(bat_iter)
#         plt.title(str(bat_iter)+"th batch" )
#         plt.xlabel("Batch Index")
#         plt.ylabel("PPG Modified Voltage")
#         plt.plot(bat_signal,'b')
#         plt.plot(adap.values(),'g')
#
#         for key in sorted(mymax):
#             plt.plot(key, mymax[key], 'ro')
#
#         bat_iter += 1
#
#         new_break_num = len(gain_max)
#         if old_break_num == new_break_num:
#             break
#
#     print RR_interval
#     plt.show()
#
#
# if __name__ == "__main__":
#     main()