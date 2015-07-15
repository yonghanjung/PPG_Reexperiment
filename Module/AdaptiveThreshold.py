# -*- coding: utf-8 -*-

# Computing Module
import numpy as np
import matplotlib.pyplot as plt


# DATA IMPORT
class AdaptiveThreshold:
    def __init__(self, Array_SignalinWindow, Flt_SamplingRate, Flt_AmpThreshold ):
        self.Array_PPGinWindow = np.squeeze(np.asarray(Array_SignalinWindow))
        self.Flt_SamplingRate = Flt_SamplingRate
        self.Flt_AmpThreshold = Flt_AmpThreshold

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

    def AdaptiveThreshold(self, Flt_SlopeThreshold, Flt_BackThreshold):
        # thr_old 들어가는 인수는 출발값
        Dict_MaxLoc_MaxAmp = dict()
        Dict_Loc_ThresholdAmp = dict()
        Flt_NewThreshold = 0.0
        Flt_OldThreshold = np.max(self.Array_PPGinWindow) * 0.2
        Flt_StdPPG = np.std(self.Array_PPGinWindow)
        Flt_VPeak = 0.0

        Int_PrevLoc = 0
        Int_CurrLoc = 0

        Bool_ThresholdUpdateMode = True # False : FindingPeak Mode, True : Update Threshold
        Bool_SignalCrossThreshold = False # True if Signal Cross Threshold

        for IntIdx in range(len(self.Array_PPGinWindow)):
            if IntIdx == 0:
                pass
            elif IntIdx > 0:
                Flt_PrevThreshold = Dict_Loc_ThresholdAmp[IntIdx-1]
                Flt_CurrThreshold = Flt_PrevThreshold + (Flt_SlopeThreshold * ((Flt_VPeak + Flt_StdPPG) / self.Flt_SamplingRate))
                Flt_PrevSigAmp = self.Array_PPGinWindow[IntIdx-1]
                Flt_CurrSigAmp = self.Array_PPGinWindow[IntIdx]
                Bool_SignalCrossThreshold = self.check_cross(prev_thr=Flt_PrevThreshold, prev_sig=Flt_PrevSigAmp, cur_thr=Flt_CurrThreshold, cur_sig = Flt_CurrSigAmp)
                # print IntIdx, Bool_SignalCrossThreshold, Bool_ThresholdUpdateMode, Flt_PrevThreshold, Flt_CurrThreshold


            # Initial Start
            # Threshold Update Mode
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

            # Peak Finding Mode
            elif Bool_ThresholdUpdateMode == False:
                if Flt_CurrSigAmp >= Flt_PrevSigAmp:
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_CurrSigAmp
                elif Flt_CurrSigAmp < Flt_PrevSigAmp:
                    Int_PrevLoc = Int_CurrLoc
                    Int_CurrLoc = IntIdx - 1
                    Flt_NewThreshold = Flt_PrevSigAmp + (Flt_SlopeThreshold * ((Flt_VPeak + Flt_StdPPG)/self.Flt_SamplingRate))
                    Dict_Loc_ThresholdAmp[IntIdx] = Flt_NewThreshold
                    # Off Peak finding mode
                    Bool_ThresholdUpdateMode = True
                    if Flt_PrevSigAmp > self.Flt_AmpThreshold:
                        Dict_MaxLoc_MaxAmp[Int_CurrLoc] = Flt_PrevSigAmp
                        Flt_VPeak = Flt_PrevSigAmp
                    continue
        return Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp

