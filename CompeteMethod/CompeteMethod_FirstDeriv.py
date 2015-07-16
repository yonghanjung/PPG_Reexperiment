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
from Module.LowPassFilter import LowPassFilter
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
        Array_DivisionSet, Array_TimeDivisionSet = self.Seperate_Division()
        Int_DivNum = len(Array_DivisionSet)
        Dict_ZeroCrossIdx_ZeroCrossAmp = dict()

        for Int_DivIdx in range(Int_DivNum):
            Array_BlockPPG = Array_DivisionSet[Int_DivIdx]
            Array_BlockTime = Array_TimeDivisionSet[Int_DivIdx]
            Array_InitPPG = Array_BlockPPG[:self.Int_InitSize]
            Flt_Threshold = np.mean(Array_InitPPG)
            _, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv = self.FirstDerivative(Array_BlockSignal=Array_BlockPPG, Array_BlockTime=Array_BlockTime, Flt_Threshold=Flt_Threshold)
            for Time, PeakAmp in np.c_[Array_TimeLoc, Array_PeakAmp]:
                Dict_ZeroCrossIdx_ZeroCrossAmp[Time] = PeakAmp
        return Dict_ZeroCrossIdx_ZeroCrossAmp


    def Seperate_Division(self):
        List_DivisionSet = list()
        List_TimeDivisionSet = list()
        for DivisionUnit in range(self.Int_TotalSet-1):
            Array_EachDivision = self.Array_PPGLong[DivisionUnit * 5 * self.Int_SamplingRate: (DivisionUnit+1)*5*self.Int_SamplingRate]
            Array_TimeDivision = self.Array_TimeLong[DivisionUnit * 5 * self.Int_SamplingRate: (DivisionUnit+1)*5*self.Int_SamplingRate]
            List_DivisionSet.append(Array_EachDivision)
            List_TimeDivisionSet.append(Array_TimeDivision)
        Array_DivisionSet = np.array(List_DivisionSet)
        Array_TimeDivisionSet = np.array(List_TimeDivisionSet)
        return Array_DivisionSet, Array_TimeDivisionSet


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
                    Array_PeakAmp.append(Array_BlockSignal[idx])
                    Dict_ZeroCrossIdx_ZeroCrossAmp[Flt_PeakLoc] = Array_BlockSignal[idx]
        return Dict_ZeroCrossIdx_ZeroCrossAmp, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv


if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 2
    Int_StartSec = 0
    Int_EndSec = 5
    Flt_SamplingRate = 75

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    Object_LowPassFilter = LowPassFilter(Array_Signal=Array_PPG_Long, Flt_CutOffFreq=10, Flt_SamplingRate=Flt_SamplingRate)
    Array_PPG_Long = Object_LowPassFilter.LowPassFilter()
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))

    Array_PPG = Array_PPG_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Array_Time = Array_Time_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Flt_Threshold = np.mean(Array_PPG[:2 * Flt_SamplingRate])
    Array_Threshold = np.array([Flt_Threshold] * len(Array_PPG))

    Array_DiffPPG = Array_PPG[1:] - Array_PPG[:-1]
    Array_DiffPPG = np.concatenate([np.zeros(1),Array_DiffPPG])
    Array_Zeros = np.zeros(len(Array_PPG))

    Object_FD = FDPractice(Array_PPGLong=Array_PPG_Long, Array_TimeLong=Array_Time_Long)
    Dict_ZeroCross = Object_FD.Conduct_FD()
    print Dict_ZeroCross

    PLOT = True

    if PLOT :
        plt.title("PPG")
        plt.grid()
        plt.plot(Array_Time_Long, Array_PPG_Long, label="Raw PPG")
        plt.plot(Dict_ZeroCross.keys(), Dict_ZeroCross.values(),'ro', label="Peak")
        plt.legend()
        plt.show()
