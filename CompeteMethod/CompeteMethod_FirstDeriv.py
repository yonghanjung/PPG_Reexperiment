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
''' Function or Class '''


class FirstDeriv:
    def __init__(self, Array_LongSignal, Array_LongTime):
        self.Array_LongSignal= Array_LongSignal
        self.Array_LongTime = Array_LongTime
        self.Flt_SamplingRate = 75
        self.Int_EachTrainDuration = 2 # Suggeseted
        self.Int_DivisionCut = 5 # I chose
        self.Int_DivisionLength = int(self.Int_DivisionCut * self.Flt_SamplingRate)
        self.Int_TrainLength = int(self.Int_EachTrainDuration * self.Flt_SamplingRate)
        self.Int_SignalLength = len(self.Array_LongSignal)

    def Conduct_FDPeakFind(self):

        for idx in range(self.Int_SignalLength - self.Int_DivisionLength):
            Array_DivisionSignal = self.Array_LongSignal[idx : idx + self.Int_DivisionLength]
            Array_DivisionTime = self.Array_LongTime[idx : idx + self.Int_DivisionLength]
            Array_InitialSignal = self.Array_LongSignal[idx : idx + self.Int_TrainLength]
            Flt_Threshold = np.mean(Array_InitialSignal)
            Dict_ZeroCrossTime_ZeroCrossAmp, Array_FirstDeriv = self.FirstDerivative(Array_Signal=Array_DivisionSignal, Flt_Threshold=Flt_Threshold)
            Array_ZeroCrossTime = list(Dict_ZeroCrossTime_ZeroCrossAmp.keys())
            Array_ZeroCrossAmp = list(Dict_ZeroCrossTime_ZeroCrossAmp.values())





    def Detect_ZeroCross(self, Flt_CurrDiffSigAmp, Flt_NextDiffSigAmp):
        if Flt_CurrDiffSigAmp > 0 and Flt_NextDiffSigAmp < 0:
            return True
        else:
            return False

    def FirstDerivative(self, Array_Signal, Array_Time, Flt_Threshold):
        Dict_ZeroCrossIdx_ZeroCrossAmp = dict()
        Array_FirstDeriv =  Array_Signal[1:] - Array_Signal[:-1]
        Int_DiffLength = len(Array_FirstDeriv)
        for idx in range(Int_DiffLength - 1):
            Flt_CurrDiffSigAmp = Array_FirstDeriv[idx]
            Flt_NextDiffSigAmp = Array_FirstDeriv[idx+1]
            if self.Detect_ZeroCross(Flt_CurrDiffSigAmp=Flt_CurrDiffSigAmp, Flt_NextDiffSigAmp=Flt_NextDiffSigAmp):
                if Array_Signal[idx+1] > Flt_Threshold:
                    Flt_PeakLoc = Array_Time[idx+1]
                    Dict_ZeroCrossIdx_ZeroCrossAmp[Flt_PeakLoc] = Array_Signal[idx+1]
        return Dict_ZeroCrossIdx_ZeroCrossAmp, Array_FirstDeriv




if __name__ == "__main__":
    T = np.linspace(0,10,100)
    Freq1 = 3
    Freq2 = 5
    Flt_Delta = 0.5
    Y = np.cos(2*np.pi*Freq1* T) + np.sin(2*np.pi*Freq2 * T)

    Object_FD = FirstDeriv(Array_Signal=Y)
    Dict_ZeroCross, Array_FirstDeriv = Object_FD.FirstDerivative()
    print Dict_ZeroCross

    plt.figure()
    plt.plot(T, Y)
    # plt.plot(T[1:], Array_FirstDeriv, 'g')
    plt.plot(T[Dict_ZeroCross.keys()], Dict_ZeroCross.values(),'ro')
    plt.grid()
    plt.show()
