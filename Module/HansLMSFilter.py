# -*- coding: utf-8 -*-
'''
Goal : 
Author : Yonghan Jung, ISyE, KAIST 
Date : 150714
Comment 
- 

'''

''' Library '''
import numpy as np
import matplotlib.pyplot as plt

''' Function or Class '''


class LMSFilter:
    def __init__(self, Array_Signal, Int_FilterLength, Flt_Stepsize):
        self.Array_Signal = np.array(Array_Signal)
        self.Int_SignalLength = len(Array_Signal)
        self.Int_FilterLength = Int_FilterLength
        # Initial Weight
        self.Array_Weight = np.zeros(Int_FilterLength)
        self.Flt_Stepsize = Flt_Stepsize


    def Compute_EachFilterEstimate(self, Array_Weight, Array_SignalinWindow, Flt_Obs):
        Flt_Estimate = np.dot(Array_Weight, Array_SignalinWindow)
        Direction = (Flt_Obs - Flt_Estimate) / np.dot(Array_SignalinWindow, Array_SignalinWindow)
            # clip to cmax ?
        Array_Weight += self.Flt_Stepsize * Direction * Array_SignalinWindow
        # print "LMS: yest %-6.3g   y %-6.3g   err %-5.2g   c %.2g" % (
        #         Flt_Estimate, Flt_Obs, Flt_Estimate - Flt_Obs, Direction )
        return Flt_Estimate, Array_Weight, Direction

    def Conduct_LMSFilter(self):
        Array_Weight = self.Array_Weight
        Array_Est = list()
        for IntIdx in xrange(self.Int_SignalLength - self.Int_FilterLength):
            Array_SignalinWindow = self.Array_Signal[IntIdx : IntIdx+self.Int_FilterLength]
            Flt_Obs = self.Array_Signal[IntIdx+self.Int_FilterLength]
            Flt_Est, Array_Weight, Direction = self.Compute_EachFilterEstimate(Array_Weight=Array_Weight, Array_SignalinWindow=Array_SignalinWindow, Flt_Obs=Flt_Obs)
            print Flt_Est
            Array_Est.append(Flt_Est)

        Array_Est = np.array(Array_Est)
        return Array_Est

def GeneratingSignal( n, f0=2, f1=40, t1=1 ):  # <-- your test function here
    # from $scipy/signal/waveforms.py
    t = np.arange( n + 0. ) / n * t1
    return np.sin( 2*np.pi * f0 * (f1/f0)**t )




if __name__ == "__main__":
    Int_SignalLength = 500
    Array_Signal = GeneratingSignal(Int_SignalLength)
    Int_FilterLength = 10
    Flt_Stepsize = 0.1
    noise = .05 * 2  # * swing
    np.random.seed(0)
    Array_Signal += np.random.normal( scale=noise, size=Int_SignalLength )  # laplace ...
    Array_Signal *= 10

    Object_LMSFilter = LMSFilter(Array_Signal=Array_Signal,Int_FilterLength=Int_FilterLength,Flt_Stepsize=Flt_Stepsize)
    Array_DenoisedSignal = Object_LMSFilter.Conduct_LMSFilter()



    # plt.plot(Array_Signal,'b')
    # plt.plot(Array_DenoisedSignal,'r')
    # plt.show()

