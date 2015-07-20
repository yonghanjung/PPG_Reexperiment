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
        Int_DivLength = 75*5
        Dict_ZeroCrossIdx_ZeroCrossAmp = dict()
        List_AllMaxIdx = list()

        for Int_DivIdx in range(Int_DivNum):
            Array_BlockPPG = Array_DivisionSet[Int_DivIdx]
            Array_BlockTime = Array_TimeDivisionSet[Int_DivIdx]
            Array_InitPPG = Array_BlockPPG[:self.Int_InitSize]
            Flt_Threshold = np.mean(Array_InitPPG)
            _, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv, List_MaxIdx = self.FirstDerivative(Array_BlockSignal=Array_BlockPPG, Array_BlockTime=Array_BlockTime, Flt_Threshold=Flt_Threshold)
            Array_MaxIdx = np.array(List_MaxIdx)
            for Idx, Time, PeakAmp in np.c_[Array_MaxIdx, Array_TimeLoc, Array_PeakAmp]:
                Dict_ZeroCrossIdx_ZeroCrossAmp[Time] = PeakAmp
                InputIdx = int(Int_DivIdx * Int_DivLength + Idx) + 1
                List_AllMaxIdx.append(InputIdx)
        return Dict_ZeroCrossIdx_ZeroCrossAmp, List_AllMaxIdx

    def Load_Answer(self, Str_DataName, Int_DataNum):
        if Str_DataName == "PPG_KW_long":
            Str_AnnoName = "../Data/" + str(Int_DataNum) + "_Anno.txt"
            List_Anno = file(Str_AnnoName,'r').read()
            List_Anno = List_Anno.split("\n")
            List_Anno = [int(x) for x in List_Anno]
            Array_Anno = np.array(List_Anno)
            Array_Anno = np.unique(Array_Anno)
        elif Str_DataName == "PPG_Walk":
            Str_AnnoName = "../Data/" + Str_DataName + str(Int_DataNum)+ "_Anno.txt"
            List_Anno = file(Str_AnnoName,'r').read()
            List_Anno = List_Anno.split("\n")
            List_Anno = [int(x) for x in List_Anno]
            Array_Anno = np.array(List_Anno)
            Array_Anno = np.unique(Array_Anno)
        return Array_Anno

    def Check_Result(self, Str_DataName, Int_DataNum, List_PeakIdx):
        Array_MyAnswer = np.array(List_PeakIdx)
        Array_MyAnswer = np.unique(Array_MyAnswer)
        Array_Anno = self.Load_Answer(Str_DataName, Int_DataNum)


        Int_TP = 0
        Int_FP = 0
        Int_FN = 0

        Int_BufferSize = 3
        for myanswer in Array_MyAnswer:
            Array_BufferMyAnswer = range(myanswer-Int_BufferSize, myanswer + Int_BufferSize)
            Array_BufferMyAnswer = np.array(Array_BufferMyAnswer)
            Array_InorNOT = np.in1d(Array_BufferMyAnswer, Array_Anno)
            if True in Array_InorNOT:
                Int_TP += 1
            elif True not in Array_InorNOT:
                Int_FP += 1

        for trueanswer in Array_Anno:
            Array_BufferMyAnswer = range(trueanswer - Int_BufferSize, trueanswer + Int_BufferSize)
            Array_BufferMyAnswer = np.array(Array_BufferMyAnswer)
            Array_InorNOT = np.in1d(Array_BufferMyAnswer, Array_MyAnswer)
            if True not in Array_InorNOT:
                Int_FN += 1

        Flt_Se = float(Int_TP) / float(Int_TP + Int_FN)
        Flt_PP = float(Int_TP) / float(Int_TP + Int_FP)
        return Str_DataName, Int_DataNum, Flt_Se, Flt_PP


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
        List_MaxIdx = list()
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
                    List_MaxIdx.append(idx)
        return Dict_ZeroCrossIdx_ZeroCrossAmp, Array_TimeLoc, Array_PeakAmp, Array_FirstDeriv, List_MaxIdx


if __name__ == "__main__":
    # Str_DataName = "PPG_KW_long"
    Str_DataName = "PPG_Walk"
    Int_DataNum = 6
    Int_StartSec = 0
    Int_EndSec = 60
    Flt_SamplingRate = 75

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    # Object_LowPassFilter = LowPassFilter(Array_Signal=Array_PPG_Long, Flt_CutOffFreq=10, Flt_SamplingRate=Flt_SamplingRate)
    # Array_PPG_Long = Object_LowPassFilter.LowPassFilter()
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))

    Array_PPG = Array_PPG_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Array_Time = Array_Time_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Flt_Threshold = np.mean(Array_PPG[:2 * Flt_SamplingRate])
    Array_Threshold = np.array([Flt_Threshold] * len(Array_PPG))

    Array_DiffPPG = Array_PPG[1:] - Array_PPG[:-1]
    Array_DiffPPG = np.concatenate([np.zeros(1),Array_DiffPPG])
    Array_Zeros = np.zeros(len(Array_PPG))

    Object_FD = FDPractice(Array_PPGLong=Array_PPG_Long, Array_TimeLong=Array_Time_Long)
    Dict_ZeroCross, List_MaxIdx  = Object_FD.Conduct_FD()
    Array_Anno = Object_FD.Load_Answer(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum)

    print Object_FD.Check_Result(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum, List_PeakIdx=List_MaxIdx)
    # print List_MaxIdx

    PLOT = True

    if PLOT :
        plt.title("FD / " + Str_DataName + str(Int_DataNum))
        plt.grid()
        plt.plot(Array_Time, Array_PPG, label="Raw PPG")
        plt.scatter(Array_Time[np.array(List_MaxIdx)], Array_PPG[np.array(List_MaxIdx)], marker='o', c='r', s = 80)
        # plt.plot(Array_Time[Array_Anno], Array_PPG[Array_Anno],'ro')
        # plt.plot(Dict_ZeroCross.keys(), Dict_ZeroCross.values(),'ro', label="Peak")
        # plt.legend()
        plt.show()
