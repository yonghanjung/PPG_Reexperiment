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


class LCMMethod:
    def __init__(self, Array_Signal, Array_Time):
        self.Array_Signal = Array_Signal
        self.Array_Time = Array_Time
        self.Int_SignalLength = len(self.Array_Signal)
    def Detect_Peak(self, Flt_Delta):
        Flt_MaxThreshold = -np.infty
        Flt_MinThreshold = np.infty
        Flt_MaxTimeLoc = 0
        Flt_MinTimeLoc = 0
        Mode_MaxFind = True
        Dict_MaxTimeLoc_MaxAmp = dict()
        Dict_MinTimeLoc_MinAmp = dict()

        for IntIdx in range(self.Int_SignalLength):
            Flt_CurrSigAmp = self.Array_Signal[IntIdx]
            if Flt_CurrSigAmp > Flt_MaxThreshold:
                Flt_MaxThreshold = Flt_CurrSigAmp
                Flt_MaxTimeLoc = self.Array_Time[IntIdx]

            if Flt_CurrSigAmp < Flt_MinThreshold:
                Flt_MinThreshold = Flt_CurrSigAmp
                Flt_MinTimeLoc = self.Array_Time[IntIdx]

            if Mode_MaxFind == True:
                if Flt_CurrSigAmp < Flt_MaxThreshold - Flt_Delta:
                    Dict_MaxTimeLoc_MaxAmp[Flt_MaxTimeLoc] = Flt_MaxThreshold
                    Flt_MinThreshold = Flt_CurrSigAmp
                    Flt_MinTimeLoc = self.Array_Time[IntIdx]
                    Mode_MaxFind = False
            elif Mode_MaxFind == False:
                if Flt_CurrSigAmp > Flt_MinThreshold + Flt_Delta:
                    Dict_MinTimeLoc_MinAmp[Flt_MinTimeLoc] = Flt_MinThreshold
                    Flt_MaxThreshold = Flt_CurrSigAmp
                    Flt_MaxTimeLoc = self.Array_Time[IntIdx]
                    Mode_MaxFind = True

        return Dict_MaxTimeLoc_MaxAmp

if __name__ == "__main__":
    T = np.linspace(0,10,100)
    Freq1 = 3
    Freq2 = 5
    Flt_Delta = 0.5
    Y = np.cos(2*np.pi*Freq1* T) + np.sin(2*np.pi*Freq2 * T)

    Objec_LCM = LCMMethod(Array_Signal=Y, Array_Time=T)
    Dict_MaxLoc_MaxAmp = Objec_LCM.Detect_Peak(Flt_Delta)

    plt.figure()
    plt.grid()
    plt.plot(T,Y)
    plt.plot(Dict_MaxLoc_MaxAmp.keys(), Dict_MaxLoc_MaxAmp.values(),'ro')
    plt.show()
