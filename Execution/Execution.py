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
import scipy as sp
import pandas as pd
from Module.data_call import data_call
from Module.bandpass import BandPassFilter
from Module.AdaptiveThreshold import AdaptiveThreshold
from Module.FourierTransformation import FourierTransformation
from Module.SlopeSumFunction import SlopeSumFunction
import adaptfilt

import matplotlib.pyplot as plt


''' Function or Class '''

class DrMPPGAnalysis:
    def __init__(self, Str_DataName, Int_DataNum, ):
        self.FltSamplingRate = 75.0
        self.Str_DataName = Str_DataName
        self.Int_DataNum = Int_DataNum
        self.Array_PPG= data_call(data_name=self.Str_DataName,data_num=self.Int_DataNum, wanted_length=0)
        self.Array_TimeDomain = np.linspace(0, len(self.Array_PPG) / self.FltSamplingRate ,len(self.Array_PPG) )

        ## CONTROL VARIABLE ##
        Int_Start = 40
        Int_End = 43
        self.Array_PPG = self.Array_PPG[ Int_Start *int(self.FltSamplingRate)   :Int_End * int(self.FltSamplingRate)]

        self.Array_TimeDomain = self.Array_TimeDomain[Int_Start *int(self.FltSamplingRate)   :Int_End * int(self.FltSamplingRate)]
        self.Flt_LowCut = 0.0
        self.Flt_HighCut = 9.0
        self.Int_BandPassOrder = 5


        #####################

    def BandPassFilter(self):
        Object_BandPassFilter = BandPassFilter(Array_Signal=self.Array_PPG, Flt_SamplingRate=self.FltSamplingRate, Flt_LowCut=self.Flt_LowCut, Flt_HighCut=self.Flt_HighCut, Int_BandPassOrder=self.Int_BandPassOrder)
        return Object_BandPassFilter.butter_bandpass_filter()

    def ConvertFrequencyDomain(self):
        Object_FFT = FourierTransformation(Array_Signal=self.Array_PPG, Flt_SamplingRate=self.FltSamplingRate)
        Array_FrequencyDomain, Array_FourierResult= Object_FFT.Compute_FrequencyDomain()
        return Array_FrequencyDomain, Array_FourierResult

    def ConvertInvertFourier(self):
        ### ControlVaraible ###
        # Source = Raghu Ram et al., (2012) A Noven Approach for Motion Artifact Reduction in PPG Signals Based on AS-LMS Adaptive Filter
        Flt_Pulsatile_Lower = 0.5
        Flt_Pulsatile_Upper = 4.0
        Flt_Resp_Lower = 0.2
        Flt_Resp_Upper = 0.35
        Flt_BandPassFilter = 9.0
        ##############################
        Array_Signal = self.Array_PPG
        # Array_Signal = self.BandPassFilter()
        NormalizedTerm = (len(self.Array_PPG)/ 2)
        Object_FFT = FourierTransformation(Array_Signal=Array_Signal, Flt_SamplingRate=self.FltSamplingRate)
        Array_FrequencyDomain, Array_FourierResult = Object_FFT.Compute_FrequencyDomain()
        for IntIdx in range(len(Array_FrequencyDomain)):
            # Cut Resp Power
            Hz = Array_FrequencyDomain[IntIdx]
            if Hz > Flt_Resp_Lower and Hz < Flt_Resp_Upper:
                Array_FourierResult[IntIdx] = 0.0
            elif Hz > Flt_Pulsatile_Lower and Hz < Flt_Pulsatile_Upper:
                Array_FourierResult[IntIdx] = 0.0
            # elif Hz <= 0.05:
            #     Array_FourierResult[IntIdx] = 0.0
            # elif Hz > Flt_BandPassFilter :
            #     Array_FourierResult[IntIdx] = 0.0
        Array_InverseFourierSignal = 2*np.fft.ifft(Array_FourierResult*NormalizedTerm).real
        return Array_FrequencyDomain, Array_FourierResult, Array_InverseFourierSignal

    def Removing_MotionArtifact(self, Int_FilterLength):
        Array_Signal = self.Array_PPG
        # Array_Signal = self.BandPassFilter()
        _,_,Array_NoiseReference = self.ConvertInvertFourier()
        Array_FilteredPPG = self.BandPassFilter()
        Flt_StepSize = 0.1

        Array_NoiseEst, Array_NoiseRemoved, Array_FilterCoefs = adaptfilt.nlms(u=Array_NoiseReference,d=Array_Signal, M=Int_FilterLength, step=Flt_StepSize)
        # Array_NoiseRemovedSignal = np.concatenate([Array_Signal[:Int_FilterLength-1], Array_NoiseRemoved])
        return Array_NoiseRemoved

    def Computing_SSF(self):
        Int_SSF_FilterLength = 10
        Int_MAR_FilterLength = 10
        Array_Signal = self.Removing_MotionArtifact(Int_MAR_FilterLength)
        Array_Signal = Array_Signal[2*Int_MAR_FilterLength:]
        Object_SSF = SlopeSumFunction(Array_SignalInWindow=Array_Signal, Int_SSFLength=Int_SSF_FilterLength)
        return Object_SSF.Conduct_SSF()

    def AdaptiveThreshold(self):
        ## Control Variable
        Flt_SlopeThreshold = -0.5
        Flt_BackThreshold = 0.4 * self.FltSamplingRate
        #####################

        Array_Signal = self.Computing_SSF()
        Object_AdaptiveThreshold = AdaptiveThreshold(Array_SignalinWindow=Array_Signal, Flt_SamplingRate=self.FltSamplingRate)
        Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp = Object_AdaptiveThreshold.AdaptiveThreshold(Flt_SlopeThreshold, Flt_BackThreshold)
        return Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp




if __name__ == "__main__":
    Str_DataName = "PPG_Walk"
    List_DataNum = [1,2,3,4,5,6,7]
    Int_DataNum = 6
    Int_FilterLength = 10
    Object_DrMPPG = DrMPPGAnalysis(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum)
    Array_TimeDomain = Object_DrMPPG.Array_TimeDomain

    Array_RawPPG = Object_DrMPPG.Array_PPG
    Array_FilteredPPG = Object_DrMPPG.BandPassFilter()
    Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp = Object_DrMPPG.AdaptiveThreshold()
    Array_FrequencyDomain, Array_FourierResult = Object_DrMPPG.ConvertFrequencyDomain()
    Array_CutFreqDomain, Array_CutFourierResult, Array_NoiseReference = Object_DrMPPG.ConvertInvertFourier()
    Array_NoiseRemovedSignal = Object_DrMPPG.Removing_MotionArtifact(Int_FilterLength=Int_FilterLength)
    Array_SSF = Object_DrMPPG.Computing_SSF()

    print len(Array_NoiseRemovedSignal)


    PLOT = True
    # PLOT = False

    if PLOT == True :
        plt.figure()
        plt.title("Raw PPG and Filtered PPG")
        plt.grid()
        plt.plot(Array_TimeDomain,Array_RawPPG,'b',label="Raw PPG")
        # plt.plot(Array_TimeDomain,Array_FilteredPPG,'r',label = "Filtered PPG")
        # plt.plot(Array_NoiseReference,'g', label="Inverse PPG")
        # plt.plot(Array_TimeDomain,Array_NoiseRemovedSignal,'g', label="Noise Removed PPG")
        plt.legend()

        plt.figure()
        plt.title("MA removed PPG")
        plt.grid()
        plt.plot(Array_TimeDomain[Int_FilterLength-1:], Array_NoiseRemovedSignal, label="Noise Removed")
        plt.legend

        plt.figure()
        plt.title("Frequency Analysis of MA reduced PPG")
        plt.stem(Array_CutFreqDomain, Array_CutFourierResult)
        plt.grid()

        plt.figure()
        plt.title("SSF")
        plt.plot(Array_SSF)
        plt.plot(Dict_Loc_ThresholdAmp.keys(), Dict_Loc_ThresholdAmp.values(),'g')
        plt.plot(Dict_MaxLoc_MaxAmp.keys(), Dict_MaxLoc_MaxAmp.values(),'ro')
        plt.grid()


        # plt.figure()
        # plt.title("Adaptive Threshold")
        # plt.grid()
        # plt.plot(Array_FilteredPPG,'b', label="Filtered PPG")
        # plt.plot(Dict_Loc_ThresholdAmp.keys(), Dict_Loc_ThresholdAmp.values(),'g', label="Threhsold")
        # plt.plot(Dict_MaxLoc_MaxAmp.keys(), Dict_MaxLoc_MaxAmp.values(),'ro', label="Peak")

        plt.show()