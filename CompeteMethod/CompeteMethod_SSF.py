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
        # self.Flt_InitThreshold =0.1* np.max(self.Array_Signal[:3 * self.Int_SamplingRate])

        Object_SlopeSum = SlopeSumFunction(self.Array_Signal,self.Int_SSFLength)
        self.Array_SlopeSumSignal, _ = Object_SlopeSum.Conduct_SSF()
        self.Flt_InitThreshold =0.6* np.max(self.Array_SlopeSumSignal[:3 * self.Int_SamplingRate])

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
        List_MaxIdx = list()

        for IntIdx in range(1,self.Int_SignalLength-1):
            Flt_PrevAmp = self.Array_SlopeSumSignal[IntIdx-1]
            Flt_CurrAmp = self.Array_SlopeSumSignal[IntIdx]
            Flt_NextAmp = self.Array_SlopeSumSignal[IntIdx+1]
            if self.Determine_PeakorNot(PrevAmp=Flt_PrevAmp, CurAmp=Flt_CurrAmp, NextAmp=Flt_NextAmp) == True:
                if len(Array_Recent_5_PeakAmp) < 5:
                    if Flt_CurrAmp > Flt_Threshold:
                        Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                        List_MaxIdx.append(IntIdx)
                        Flt_CurrAmp = self.Array_SlopeSumSignal[IntIdx]
                        Dict_PeakIdxLoc_PeakAmp[Flt_MaxTimeLoc] = Flt_CurrAmp
                        Array_Recent_5_PeakAmp.append(Flt_CurrAmp)
                elif len(Array_Recent_5_PeakAmp) == 5:
                    Flt_Threshold = 0.7*np.median(Array_Recent_5_PeakAmp)
                    if Flt_CurrAmp > Flt_Threshold:
                        Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                        List_MaxIdx.append(IntIdx)
                        Flt_CurrAmp = self.Array_SlopeSumSignal[IntIdx]
                        Dict_PeakIdxLoc_PeakAmp[Flt_MaxTimeLoc] = Flt_CurrAmp
                        Array_Recent_5_PeakAmp.pop(0)
                        Array_Recent_5_PeakAmp.append(Flt_CurrAmp)
            Array_Threshold.append(Flt_Threshold)
        Array_Threshold.append(Flt_Threshold)

        return Dict_PeakIdxLoc_PeakAmp, Array_Threshold, np.array(List_MaxIdx)


if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    # Str_DataName = "PPG_Walk"
    Int_DataNum = 2
    Flt_SamplingRate = 75
    Flt_highCut = 11
    Flt_LowCut = 0.5
    Int_OneMinCut = 60*75

    PLOT = True

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))

    Array_PPG = Array_PPG_Long[:Int_OneMinCut]
    Array_Time = Array_Time_Long[:Int_OneMinCut]

    # Object_LowPassFilter = BandPassFilter(Array_Signal=Array_PPG_Long,Flt_SamplingRate=Flt_SamplingRate, Flt_LowCut=Flt_LowCut, Flt_HighCut=Flt_highCut)
    # Array_PPG_Long = Object_LowPassFilter.butter_bandpass_filter()
    Object_SSF = SSFMethod(Array_Signal=Array_PPG, Array_Time=Array_Time)
    Dict_PeakIdxLoc_PeakAmp, Array_Threshold, List_MaxIdx = Object_SSF.Conduct_PeakDetect()

    print Object_SSF.Check_Result(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum, List_PeakIdx=List_MaxIdx)

    if PLOT:
        plt.figure()
        plt.title("SSF / " + Str_DataName + str(Int_DataNum))
        plt.grid()
        plt.plot(Array_Time, Array_PPG,'b',label = "Raw PPG")
        plt.plot(Array_Time, Array_Threshold,'g--', label="Threshold")
        # plt.plot(Dict_PeakIdxLoc_PeakAmp.keys(), Dict_PeakIdxLoc_PeakAmp.values(),'ro', label="PEAK")
        plt.plot(Array_Time[List_MaxIdx], Array_PPG[List_MaxIdx],'ro')
        plt.legend()
        plt.show()
