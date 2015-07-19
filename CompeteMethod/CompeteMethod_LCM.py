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
from Module.bandpass import BandPassFilter
''' Function or Class '''


class LCMMethod:
    def __init__(self, Array_Signal, Array_Time):
        self.Array_Signal = Array_Signal
        self.Array_Time = Array_Time
        self.Int_SignalLength = len(self.Array_Signal)
        # Object_BandPassFilter = BandPassFilter(Array_Signal=self.Array_Signal, Flt_LowCut=0.5, Flt_HighCut=8.0, Flt_SamplingRate=75)
        # self.Array_Signal = Object_BandPassFilter.butter_bandpass_filter()

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
        # # print Array_MyAnswer
        # if Str_DataName == "PPG_KW_long":
        #     Str_AnnoName = "../Data/" + str(Int_DataNum) + "_Anno.txt"
        #     List_Anno = file(Str_AnnoName,'r').read()
        #     List_Anno = List_Anno.split("\n")
        #     List_Anno = [int(x) for x in List_Anno]
        #     Array_Anno = np.array(List_Anno)
        #     Array_Anno = np.unique(Array_Anno)
        # elif Str_DataName == "PPG_Walk":
        #     Str_AnnoName = "../Data/" + Str_DataName + str(Int_DataNum)+ "_Anno.txt"
        #     List_Anno = file(Str_AnnoName,'r').read()
        #     List_Anno = List_Anno.split("\n")
        #     List_Anno = [int(x) for x in List_Anno]
        #     Array_Anno = np.array(List_Anno)
        #     Array_Anno = np.unique(Array_Anno)

        Int_TP = 0
        Int_FP = 0
        Int_FN = 0

        for myanswer in Array_MyAnswer:
            if myanswer in Array_Anno:
                Int_TP += 1
            elif myanswer not in Array_Anno:
                Int_FP += 1

        for trueanswer in Array_Anno:
            if trueanswer not in Array_MyAnswer:
                Int_FN += 1

        Flt_Se = float(Int_TP) / float(Int_TP + Int_FN)
        Flt_PP = float(Int_TP) / float(Int_TP + Int_FP)
        return Str_DataName, Int_DataNum, Flt_Se, Flt_PP

    def Detect_Peak(self, Flt_Delta):
        Flt_MaxThreshold = -np.infty
        Flt_MinThreshold = np.infty
        Flt_MaxTimeLoc = 0
        Flt_MinTimeLoc = 0
        Mode_MaxFind = True
        Dict_MaxTimeLoc_MaxAmp = dict()
        Dict_MinTimeLoc_MinAmp = dict()
        Array_PeakIdx = list()

        for IntIdx in range(self.Int_SignalLength):
            Flt_CurrSigAmp = self.Array_Signal[IntIdx]
            if Flt_CurrSigAmp > Flt_MaxThreshold:
                Flt_MaxThreshold = Flt_CurrSigAmp
                Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                Int_MaxLoc = IntIdx

            if Flt_CurrSigAmp < Flt_MinThreshold:
                Flt_MinThreshold = Flt_CurrSigAmp
                Flt_MinTimeLoc = self.Array_Time[IntIdx]

            if Mode_MaxFind == True:
                if Flt_CurrSigAmp < Flt_MaxThreshold - Flt_Delta:
                    Array_PeakIdx.append(Int_MaxLoc)
                    Dict_MaxTimeLoc_MaxAmp[Flt_MaxTimeLoc] = Flt_MaxThreshold
                    Flt_MinThreshold = Flt_CurrSigAmp
                    Flt_MinTimeLoc = self.Array_Time[IntIdx]
                    Mode_MaxFind = False
            elif Mode_MaxFind == False:
                if Flt_CurrSigAmp > Flt_MinThreshold + Flt_Delta:
                    Dict_MinTimeLoc_MinAmp[Flt_MinTimeLoc] = Flt_MinThreshold
                    Flt_MaxThreshold = Flt_CurrSigAmp
                    Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                    Int_MaxLoc = IntIdx
                    Mode_MaxFind = True

        return Dict_MaxTimeLoc_MaxAmp, Array_PeakIdx

if __name__ == "__main__":
    Str_DataName = "PPG_Walk"
    Str_DataName = 'PPG_KW_long'
    Int_DataNum = 2
    Int_SamplingRate = 75
    Flt_Delta = 1
    Int_OneMinCut = 60*75

    Array_PPG = data_call(data_name=Str_DataName, data_num=Int_DataNum,wanted_length=0)
    Array_Time = np.linspace(0,len(Array_PPG) /float(Int_SamplingRate),len(Array_PPG))
    Array_PPG = Array_PPG[:Int_OneMinCut]
    Array_Time = Array_Time[:Int_OneMinCut]
    Array_PPG = np.array(Array_PPG)
    Array_Time = np.array(Array_Time)

    Object_BandPass = BandPassFilter(Array_Signal=Array_PPG,Flt_HighCut=8.0, Flt_LowCut=0.5, Flt_SamplingRate=75 )
    # Array_PPG = Object_BandPass.butter_bandpass_filter()

    Objec_LCM = LCMMethod(Array_Signal=Array_PPG, Array_Time=Array_Time)
    Dict_MaxLoc_MaxAmp, Array_PeakIdx = Objec_LCM.Detect_Peak(Flt_Delta)
    Array_Anno = Objec_LCM.Load_Answer(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum)
    Array_Anno = list(Array_Anno)

    print Objec_LCM.Check_Result(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum, List_PeakIdx=Array_PeakIdx)

    plt.figure()
    plt.title("LCM / " + Str_DataName + str(Int_DataNum))
    plt.grid()
    plt.plot(Array_Time,Array_PPG, label="Raw PPG")
    plt.plot(Array_Time[np.array(Array_PeakIdx)], Array_PPG[np.array(Array_PeakIdx)],'bo')
    plt.plot(Array_Time[Array_Anno], Array_PPG[Array_Anno],'ro')
    plt.legend()
    plt.show()
