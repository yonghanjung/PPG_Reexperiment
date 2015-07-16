# -*- coding: utf-8 -*-
'''
Goal : 
Author : Yonghan Jung, ISyE, KAIST 
Date : 15
Comment 
- 

'''

''' Library '''
import numpy as np
import matplotlib.pyplot as plt
from Module.data_call import data_call
''' Function or Class '''


class FDPractice:
    def __init__(self, Array_PPGLong, Array_TimeLong):
        self.Array_PPGLong = Array_PPGLong
        self.Array_TimeLong = Array_TimeLong
        self.Int_SeperateSize = 5 * 75
        self.Int_TotalSet = 12
        self.Int_InitSize = 2* 75
        self.Int_SamplingRate = 75

    def Conduct_FD(self):
        pass

    def Seperate_Division(self):
        List_DivisionSet = list()
        List_TimeDivisionSet = list()
        for DivisionUnit in range(self.Int_TotalSet-1):
            Array_EachDivision = self.Array_PPGLong[DivisionUnit * self.Int_SamplingRate: DivisionUnit*self.Int_SamplingRate]
            Array_TimeDivision = self.Array_TimeLong[DivisionUnit * self.Int_SamplingRate: DivisionUnit*self.Int_SamplingRate]
            List_DivisionSet.append(Array_EachDivision)
            List_TimeDivisionSet.append(Array_TimeDivision)
        List_DivisionSet = np.array(List_DivisionSet)
        List_TimeDivisionSet = np.array(List_TimeDivisionSet)
        return List_DivisionSet, List_TimeDivisionSet


    def Detect_ZeroCross(self, Flt_CurrDiffSigAmp, Flt_NextDiffSigAmp):
        if Flt_CurrDiffSigAmp > 0 and Flt_NextDiffSigAmp < 0:
            return True
        else:
            return False

    def FirstDerivative(self, Array_BlockSignal, Array_BlockTime, Flt_Threshold):
        Array_PeakAmp = list()
        Array_TimeLoc = list()
        Dict_ZeroCrossIdx_ZeroCrossAmp = dict()
        Array_FirstDeriv =  Array_BlockSignal[1:] - Array_BlockSignal[:-1]
        Int_DiffLength = len(Array_FirstDeriv)
        for idx in range(Int_DiffLength - 1):
            Flt_CurrDiffSigAmp = Array_FirstDeriv[idx]
            Flt_NextDiffSigAmp = Array_FirstDeriv[idx+1]
            if self.Detect_ZeroCross(Flt_CurrDiffSigAmp=Flt_CurrDiffSigAmp, Flt_NextDiffSigAmp=Flt_NextDiffSigAmp):
                if Array_BlockSignal[idx] > Flt_Threshold:
                    Flt_PeakLoc = Array_BlockTime[idx]
                    Array_TimeLoc.append(Flt_PeakLoc)
                    Array_PeakAmp = Array_BlockSignal[idx]
                    Dict_ZeroCrossIdx_ZeroCrossAmp[Flt_PeakLoc] = Array_BlockSignal[idx]
        return Dict_ZeroCrossIdx_ZeroCrossAmp, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv


if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 1
    Int_StartSec = 0
    Int_EndSec = 5
    Flt_SamplingRate = 75

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))

    Array_PPG = Array_PPG_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Array_Time = Array_Time_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Flt_Threshold = np.mean(Array_PPG[:2 * Flt_SamplingRate])
    Array_Threshold = np.array([Flt_Threshold] * len(Array_PPG))

    Array_DiffPPG = Array_PPG[1:] - Array_PPG[:-1]
    Array_DiffPPG = np.concatenate([np.zeros(1),Array_DiffPPG])
    Array_Zeros = np.zeros(len(Array_PPG))

    Object_FD = FDPractice()
    Dict_ZeroCrossIdx_ZeroCrossAmp, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv = Object_FD.FirstDerivative(Array_BlockSignal=Array_PPG, Array_BlockTime=Array_Time, Flt_Threshold=Flt_Threshold)

    PLOT = True

    if PLOT :
        plt.title("PPG")
        plt.grid()
        plt.plot(Array_Time, Array_PPG,'b', label="Raw PPG ")
        plt.plot(Array_Time, Array_DiffPPG,'g', label= "Diff PPG")
        plt.plot(Array_Time, Array_Threshold, 'g.')
        plt.plot(Array_Time, Array_Zeros,'r.')
        plt.plot(Dict_ZeroCrossIdx_ZeroCrossAmp.keys(), Dict_ZeroCrossIdx_ZeroCrossAmp.values(), 'ro')
        plt.legend()
        plt.show()
