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

import matplotlib.pyplot as plt


''' Function or Class '''

class DrMPPGAnalysis:
    def __init__(self, Str_DataName, Int_DataNum, ):
        self.Str_DataName = Str_DataName
        self.Int_DataNum = Int_DataNum
        self.Array_PPG= data_call(data_name=self.Str_DataName,data_num=self.Int_DataNum, wanted_length=0)

        ## CONTROL VARIABLE ##
        self.FltSamplingRate = 75.0
        self.Array_PPG = self.Array_PPG[:10 * int(self.FltSamplingRate)]
        self.Flt_LowCut = 0.5
        self.Flt_HighCut = 9.0
        self.Int_BandPassOrder = 5
        #####################

    def BandPassFilter(self):
        Object_BandPassFilter = BandPassFilter(Array_Signal=self.Array_PPG, Flt_SamplingRate=self.FltSamplingRate, Flt_LowCut=self.Flt_LowCut, Flt_HighCut=self.Flt_HighCut, Int_BandPassOrder=self.Int_BandPassOrder)
        return Object_BandPassFilter.butter_bandpass_filter()

    def AdaptiveThreshold(self):
        ## Control Variable
        Flt_SlopeThreshold = -0.5
        Flt_BackThreshold = 0.4 * self.FltSamplingRate
        #####################

        Array_FilteredPPG = self.BandPassFilter()
        Object_AdaptiveThreshold = AdaptiveThreshold(Array_SignalinWindow=Array_FilteredPPG, Flt_SamplingRate=self.FltSamplingRate)
        Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp = Object_AdaptiveThreshold.AdaptiveThreshold(Flt_SlopeThreshold, Flt_BackThreshold)
        return Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp

    def ConvertFrequencyDomain(self):
        Object_FFT = FourierTransformation(Array_Signal=self.Array_PPG, Flt_SamplingRate=self.FltSamplingRate)
        Array_FrequencyDomain, Array_FourierResult= Object_FFT.Compute_FrequencyDomain()
        Object_FFT.PLOT()
        return Array_FrequencyDomain, Array_FourierResult

    def MAReduction(self):
        ### ControlVaraible ###
        # Source = Raghu Ram et al., (2012) A Noven Approach for Motion Artifact Reduction in PPG Signals Based on AS-LMS Adaptive Filter
        Flt_Pulsatile_Lower = 0.5
        Flt_Pulsatile_Upper = 4.0
        Flt_Resp_Lower = 0.2
        Flt_Resp_Upper = 0.35
        ##############################






if __name__ == "__main__":
    Str_DataName = "PPG_Walk"
    List_DataNum = [1,2,3,4,5,6,7]
    Int_DataNum = 2
    Object_DrMPPG = DrMPPGAnalysis(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum)

    Array_RawPPG = Object_DrMPPG.Array_PPG
    Array_FilteredPPG = Object_DrMPPG.BandPassFilter()
    Dict_Loc_ThresholdAmp, Dict_MaxLoc_MaxAmp = Object_DrMPPG.AdaptiveThreshold()
    Array_FrequencyDomain, Array_FourierResult = Object_DrMPPG.ConvertFrequencyDomain()

    PLOT = True
    # PLOT = False

    if PLOT == True :
        plt.figure()
        plt.title("Raw PPG and Filtered PPG")
        plt.grid()
        plt.plot(Array_RawPPG,'b',label="Raw PPG")
        plt.plot(Array_FilteredPPG,'r',label = "Filtered PPG")
        plt.legend()

        plt.figure()
        plt.title("Adaptive Threshold")
        plt.grid()
        plt.plot(Array_FilteredPPG,'b', label="Filtered PPG")
        plt.plot(Dict_Loc_ThresholdAmp.keys(), Dict_Loc_ThresholdAmp.values(),'g', label="Threhsold")
        plt.plot(Dict_MaxLoc_MaxAmp.keys(), Dict_MaxLoc_MaxAmp.values(),'ro', label="Peak")


        plt.show()