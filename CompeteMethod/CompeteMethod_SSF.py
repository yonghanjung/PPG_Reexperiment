# -*- coding: utf-8 -*-
'''
Goal : 
Author : Yonghan Jung, ISyE, KAIST 
Date : 150715
Comment 
- 

'''

''' Library '''
import numpy as np
import matplotlib.pyplot as plt
from Module.data_call import data_call
from Module.SlopeSumFunction import SlopeSumFunction
from Module.bandpass import BandPassFilter

''' Function or Class '''

class SSFMethod:
    def __init__(self, Array_Signal, Array_Time):
        self.Array_Signal = Array_Signal
        self.Array_Time = Array_Time
        self.Int_SSFLength = 10
        self.Int_SignalLength = len(Array_Signal)
        self.Int_SamplingRate = 75
        self.Flt_InitThreshold =0.7* np.max(self.Array_Signal[:3 * self.Int_SamplingRate])

        Object_SlopeSum = SlopeSumFunction(self.Array_Signal,self.Int_SSFLength)
        self.Array_SlopeSumSignal, _ = Object_SlopeSum.Conduct_SSF()


    def Determine_PeakorNot(self, PrevAmp, CurAmp, NextAmp):
        if PrevAmp < CurAmp and CurAmp >= NextAmp:
            return True
        else:
            return False

    def Conduct_PeakDetect(self):
        Array_Recent_5_PeakAmp = list()
        Dict_PeakIdxLoc_PeakAmp = dict()
        Flt_Threshold = self.Flt_InitThreshold
        Array_Threshold = [Flt_Threshold]

        for IntIdx in range(1,self.Int_SignalLength-1):
            Flt_PrevAmp = self.Array_SlopeSumSignal[IntIdx-1]
            Flt_CurrAmp = self.Array_SlopeSumSignal[IntIdx]
            Flt_NextAmp = self.Array_SlopeSumSignal[IntIdx+1]
            if self.Determine_PeakorNot(PrevAmp=Flt_PrevAmp, CurAmp=Flt_CurrAmp, NextAmp=Flt_NextAmp) == True:
                if len(Array_Recent_5_PeakAmp) < 5:
                    if Flt_CurrAmp > Flt_Threshold:
                        Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                        Flt_CurrAmp = self.Array_Signal[IntIdx]
                        Dict_PeakIdxLoc_PeakAmp[Flt_MaxTimeLoc] = Flt_CurrAmp
                        Array_Recent_5_PeakAmp.append(Flt_CurrAmp)
                elif len(Array_Recent_5_PeakAmp) == 5:
                    Flt_Threshold = 0.7*np.median(Array_Recent_5_PeakAmp)
                    if Flt_CurrAmp > Flt_Threshold:
                        Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                        Flt_CurrAmp = self.Array_Signal[IntIdx]
                        Dict_PeakIdxLoc_PeakAmp[Flt_MaxTimeLoc] = Flt_CurrAmp
                        Array_Recent_5_PeakAmp.pop(0)
                        Array_Recent_5_PeakAmp.append(Flt_CurrAmp)
            Array_Threshold.append(Flt_Threshold)
        Array_Threshold.append(Flt_Threshold)

        return Dict_PeakIdxLoc_PeakAmp, Array_Threshold


if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 0
    Flt_SamplingRate = 75
    Flt_highCut = 11
    Flt_LowCut = 0.5

    PLOT = True

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))
    Object_LowPassFilter = BandPassFilter(Array_Signal=Array_PPG_Long,Flt_SamplingRate=Flt_SamplingRate, Flt_LowCut=Flt_LowCut, Flt_HighCut=Flt_highCut)
    Array_PPG_Long = Object_LowPassFilter.butter_bandpass_filter()
    Object_SSF = SSFMethod(Array_Signal=Array_PPG_Long, Array_Time=Array_Time_Long)
    Dict_PeakIdxLoc_PeakAmp, Array_Threshold = Object_SSF.Conduct_PeakDetect()

    if PLOT:
        plt.figure()
        plt.title("PPG")
        plt.grid()
        plt.plot(Array_Time_Long, Array_PPG_Long,'b',label = "Raw PPG")
        plt.plot(Array_Time_Long, Array_Threshold,'g--', label="Threshold")
        plt.plot(Dict_PeakIdxLoc_PeakAmp.keys(), Dict_PeakIdxLoc_PeakAmp.values(),'ro', label="PEAK")
        plt.legend()
        plt.show()
