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
from scipy.fftpack import rfft, irfft, fftfreq
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
        Array_FrequencyDomain = np.linspace(start=0,stop=Int_SignalLength,num = Int_SignalLength)
        # np.array(range(0,Int_SignalLength))
        # How long seconds it sampled
        Flt_HowLongSecSampled = Int_SignalLength / float(self.Flt_SamplingRate)
        # Frequency Domain (X-axis)
        Array_FrequencyDomain /= Flt_HowLongSecSampled

        # Only want the first half of FFT
        Int_CutOFF = np.ceil(Int_SignalLength/2)

        # Take the first half of the spectrum
        # Normalize data
        Array_FourierResult = np.fft.fft(self.Array_Signal) / (Int_SignalLength / 2)
        # Array_FourierResult = Array_FourierResult[:Int_CutOFF]
        Array_FourierResult[Int_CutOFF:] = 0
        # We want the size
        Array_FourierResult = np.abs(Array_FourierResult)
        # Array_FourierResult[Int_CutOFF:] = 0
        # Array_FrequencyDomain = Array_FrequencyDomain[:Int_CutOFF]

        return Array_FrequencyDomain, Array_FourierResult

    def Practice_NewFreqDomain(self):
        Int_SignalLength = len(self.Array_Signal)
        Array_FrequencyDomain = fftfreq(Int_SignalLength, d=self.Flt_SamlingTimeInterval*2.0)
        Array_FourierResult = np.fft.ifft(self.Array_Signal).real

        return Array_FrequencyDomain, Array_FourierResult


    def Compute_InverseFourier(self, Flt_CutFreq):
        Int_SignalLength = len(self.Array_Signal)
        NormalizedTerm = (Int_SignalLength / 2)
        Flt_HowLongSecSampled = Int_SignalLength / float(self.Flt_SamplingRate)
        Array_FrequencyDomain, Array_FourierResult = self.Compute_FrequencyDomain()
        Array_FourierResult[Array_FrequencyDomain < Flt_CutFreq] = 0
        Array_InverseFourierSignal = 2*np.fft.ifft(Array_FourierResult*NormalizedTerm).real
        return Array_InverseFourierSignal


    def PLOT(self):
        # Array_FrequencyDomain, Array_FourierResult = self.Compute_FrequencyDomain()
        # Array_InverseFourier = self.Compute_InverseFourier()

        plt.figure()
        plt.title("Freuqency Domain Analysis")
        plt.grid()
        plt.stem(Array_FrequencyDomain, Array_FourierResult)
        plt.xlabel("Freuqency (Hz)")
        plt.ylabel("Amplitude in Time Domain")


        pass



if __name__ == "__main__":
    Int_SamplingRate = 100

    Flt_SamplingInterval = 1/float(Int_SamplingRate)
    PLOT = True

    Array_Signal = np.linspace(0,10,Int_SamplingRate)
    Array_SamplingPeriod = np.linspace(0,1-Flt_SamplingInterval, int(Int_SamplingRate))

    Frequency = 10
    Frequency2 = 7
    Frequency3 = 5
    CutSignal = Frequency2 + 0.1

    Array_Signal1 = 5*np.cos(2*np.pi * Frequency* Array_SamplingPeriod)
    Array_Signal2 = 8*np.cos(2*np.pi * Frequency2* Array_SamplingPeriod)
    Array_Signal3 = 6*np.sin(2*np.pi * Frequency3* Array_SamplingPeriod)
    Array_Signal = Array_Signal1 + Array_Signal2 + Array_Signal3
    Array_CutSignal = Array_Signal1
    Object_FFT = FourierTransformation(Array_Signal=Array_Signal, Flt_SamplingRate=Int_SamplingRate)
    Array_ExampleSignal = Object_FFT.Array_Signal
    Array_FrequencyDomain, Array_FourierResult = Object_FFT.Compute_FrequencyDomain()
    Array_InverseFourierSignal = Object_FFT.Compute_InverseFourier(CutSignal)
    # print Array_FrequencyDomain
    # print Array_FourierResult

    for FreqDomain, HZ in zip(Array_FrequencyDomain, Array_FourierResult):
        print FreqDomain, HZ

    # Array_InverseFourier = Object_FFT.Compute_InverseFourier(Frequency2+3)
    # print Array_InverseFourier





    if PLOT :
        plt.figure()
        plt.title("Original Figure")
        plt.grid()
        plt.plot(Array_SamplingPeriod, Array_ExampleSignal)

        plt.figure()
        plt.title("Frequency")
        plt.grid()
        plt.stem(Array_FrequencyDomain, Array_FourierResult)

        plt.figure()
        plt.title("New Frequency")
        plt.grid()
        plt.plot(Array_SamplingPeriod, Array_InverseFourierSignal,'b')
        plt.plot(Array_SamplingPeriod, Array_CutSignal,'g')
        #
        # plt.figure()
        # plt.title("Inverse Fourier")
        # plt.grid()
        # plt.plot(Array_InverseFourier)

        plt.show()