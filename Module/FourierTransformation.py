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
# import numpy.fft as fft
''' Function or Class '''


class FourierTransformation:
    def __init__(self, Array_Signal, Flt_SamplingRate):
        self.Array_Signal = Array_Signal
        self.Flt_SamplingRate = Flt_SamplingRate
        self.Flt_SamlingTimeInterval = 1/ float(self.Flt_SamplingRate)
        self.Array_SamplingPeriod = np.linspace(0,1-self.Flt_SamlingTimeInterval, int(self.Flt_SamplingRate))
        self.Int_NumSamples = len(self.Array_SamplingPeriod)

    def Compute_FrequencyDomain(self):
        # To get the length
        Int_SignalLength = len(self.Array_Signal)
        # Create Vector
        Array_FrequencyDomain = np.array(range(0,Int_SignalLength))
        # How long seconds it sampled
        Flt_HowLongSecSampled = Int_SignalLength / float(self.Flt_SamplingRate)
        # Frequency Domain (X-axis)
        Array_FrequencyDomain /= Flt_HowLongSecSampled
        # Normalize data


        # Only want the first half of FFT
        Int_CutOFF = np.ceil(Int_SignalLength/2)

        # Take the first half of the spectrum
        Array_FourierResult = np.fft.fft(self.Array_Signal) / (Int_SignalLength / 2)
        Array_FourierResult = Array_FourierResult[:Int_CutOFF]
        # We want the size
        Array_FourierResult = np.abs(Array_FourierResult)
        Array_FrequencyDomain = Array_FrequencyDomain[:Int_CutOFF]

        return Array_FrequencyDomain, Array_FourierResult

    def PLOT(self):
        Array_FrequencyDomain, Array_FourierResult = self.Compute_FrequencyDomain()
        plt.figure()
        plt.title("Freuqency Domain Analysis")
        plt.grid()
        plt.stem(Array_FrequencyDomain, Array_FourierResult)
        plt.xlabel("Freuqency (Hz)")
        plt.ylabel("Amplitude in Time Domain")
        pass



if __name__ == "__main__":
    Int_SamplingRate = 300
    Frequency = 10
    Flt_SamplingInterval = 1/float(Int_SamplingRate)
    PLOT = True

    Array_Signal = np.linspace(0,10,Int_SamplingRate)
    Array_SamplingPeriod = np.linspace(0,1-Flt_SamplingInterval, int(Int_SamplingRate))
    Array_Signal = 10*np.sin(2 * np.pi * Frequency* Array_SamplingPeriod)
    Object_FFT = FourierTransformation(Array_Signal=Array_Signal, Flt_SamplingRate=Int_SamplingRate)
    Array_ExampleSignal = Object_FFT.Array_Signal
    Array_FrequencyDomain, Array_FourierResult = Object_FFT.Compute_FrequencyDomain()
    Object_FFT.PLOT()



    if PLOT :
        plt.figure()
        plt.title("Original Figure")
        plt.grid()
        plt.plot(Array_SamplingPeriod, Array_ExampleSignal)

        # plt.figure()
        # plt.title("Frequency")
        # plt.grid()
        # plt.stem(Array_FrequencyDomain, Array_FourierResult)

        plt.show()