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
''' Function or Class '''


class SlopeSumFunction:
    def __init__(self, Array_SignalInWindow, Int_SSFLength):
        self.Array_SignalInWindow = Array_SignalInWindow
        self.Int_SSFLength = Int_SSFLength
        self.Int_SignalLength = len(self.Array_SignalInWindow)

    def DerivativeSum(self, Array_SmallSignalinWindow):
        Array_Difference = Array_SmallSignalinWindow[1:] - Array_SmallSignalinWindow[:-1]
        Flt_TotalSum = np.sum(Array_Difference)

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
        return Array_SlopeSumSignal





if __name__ == "__main__":
    T = np.linspace(0,10,100)
    Y = np.cos(2* 1*np.pi * T) + 0.3*np.sin(2*5*np.pi*T)
    Int_FilterLen = 10
    Object_SSF = SlopeSumFunction(Y,Int_FilterLen)
    Array_SlopeSumSignal = Object_SSF.Conduct_SSF()

    plt.figure()
    plt.grid()
    plt.plot(T,Y)

    plt.figure()
    plt.grid()
    plt.plot(T[Int_FilterLen:], Array_SlopeSumSignal)
    plt.show()