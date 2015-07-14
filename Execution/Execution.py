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
import matplotlib.pyplot as plt

''' Function or Class '''

class DrMPPGAnalysis:
    def __init__(self, Str_DataName, Int_DataNum, ):
        self.Str_DataName = Str_DataName
        self.Int_DataNum = Int_DataNum
        self.Array_PPG= data_call(data_name=self.Str_DataName,data_num=self.Int_DataNum, wanted_length=0)
        self.FltSamplingRate = 75
        self.Flt_LowCut = 0.5
        self.Flt_HighCut = 9.0
        self.Int_BandPassOrder = 5

    def BandPassFilter(self):
        Object_BandPassFilter = BandPassFilter(Array_Signal=self.Array_PPG, Flt_SamplingRate=self.FltSamplingRate, Flt_LowCut=self.Flt_LowCut, Flt_HighCut=self.Flt_HighCut, Int_BandPassOrder=self.Int_BandPassOrder)
        return Object_BandPassFilter.butter_bandpass_filter()



if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 1
    Object_DrMPPG = DrMPPGAnalysis(Str_DataName=Str_DataName, Int_DataNum=Int_DataNum)
    Array_RawPPG = Object_DrMPPG.Array_PPG
    Array_FilteredPPG = Object_DrMPPG.BandPassFilter()

    plt.grid()
    plt.plot(Array_RawPPG,'b',label="Raw PPG")
    plt.plot(Array_FilteredPPG,'r',label = "Filtered PPG")
    plt.legend()
    plt.show()