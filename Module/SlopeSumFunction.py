# -*- coding: utf-8 -*-
'''
Goal : Construct the Slope Sum Signal
Author : Yonghan Jung, ISyE, KAIST 
Date : 150715
Comment 
- 

'''

''' Library '''
import numpy as np
import matplotlib.pyplot as plt
from Module.data_call import data_call
''' Function or Class '''


class SlopeSumFunction:
    def __init__(self, Array_SignalInWindow, Int_SSFLength):
        self.Array_SignalInWindow = Array_SignalInWindow
        self.Int_SSFLength = Int_SSFLength
        self.Int_SignalLength = len(self.Array_SignalInWindow)

    def DerivativeSum(self, Array_SmallSignalinWindow):
        Array_Difference = Array_SmallSignalinWindow[1:] - Array_SmallSignalinWindow[:-1]
        Flt_TotalSum = 0.0
        for val in Array_Difference:
            if val > 0:
                Flt_TotalSum += val
            elif val <= 0:
                Flt_TotalSum += 0.0

        # Flt_TotalSum = np.sum(Array_Difference)

        return Flt_TotalSum

    def Conduct_SSF(self):
        Array_SlopeSumSignal = list()
        for IntIdx in range(self.Int_SignalLength - self.Int_SSFLength):
            Array_SmallSignalinwindow = self.Array_SignalInWindow[IntIdx : IntIdx + self.Int_SSFLength]
            Flt_SlopsSum = self.DerivativeSum(Array_SmallSignalinWindow=Array_SmallSignalinwindow)
            if Flt_SlopsSum > 0:
                Array_SlopeSumSignal.append(Flt_SlopsSum)
            else:
                Array_SlopeSumSignal.append(0.0)
        Array_SlopeSumSignal = np.array(Array_SlopeSumSignal)
        Array_SlopeSumSignal = np.concatenate([np.zeros(self.Int_SSFLength), Array_SlopeSumSignal])
        Flt_ThresholdValue = np.max(Array_SlopeSumSignal) * 0.7
        return Array_SlopeSumSignal, Flt_ThresholdValue





if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 1
    Flt_SamplingRate = 75
    Flt_highCut = 11
    Flt_LowCut = 0.5

    Int_Start = 0 * Flt_SamplingRate
    Int_End = 5 * Flt_SamplingRate

    PLOT = True


    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG = Array_PPG_Long[Int_Start : Int_End]
    Array_PPG = np.array(Array_PPG)
    Array_Time = np.linspace(0,len(Array_PPG_Long)/75.0,len(Array_PPG_Long))
    Array_Time = Array_Time[Int_Start:Int_End]

    # T = np.linspace(0,10,100)
    # Y = np.cos(2* 1*np.pi * T) + 0.3*np.sin(2*5*np.pi*T)
    Int_FilterLen = 10
    Object_SSF = SlopeSumFunction(Array_PPG,Int_FilterLen)
    Array_SlopeSumSignal, Flt_Threshold  = Object_SSF.Conduct_SSF()


    plt.figure()
    plt.grid()
    plt.plot(Array_Time,Array_PPG)

    plt.figure()
    plt.grid()
    plt.plot(Array_Time, Array_SlopeSumSignal)
    plt.show()