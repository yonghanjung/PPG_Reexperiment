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
from Module.data_call import data_call
from Module.SlopeSumFunction import SlopeSumFunction

''' Function or Class '''

class SSFMethod:
    def __init__(self):
        return None


if __name__ == "__main__":
    Str_DataName = "PPG_KW_long"
    Int_DataNum = 2
    Int_StartSec = 0
    Int_EndSec = 5
    Flt_SamplingRate = 75

    PLOT = True

    Array_PPG_Long = data_call(data_name=Str_DataName,data_num=Int_DataNum, wanted_length=0)
    Array_PPG_Long = np.array(Array_PPG_Long)
    Array_Time_Long = np.linspace(0,len(Array_PPG_Long)/Flt_SamplingRate,len(Array_PPG_Long))

    Array_PPG = Array_PPG_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]
    Array_Time = Array_Time_Long[Int_StartSec * Flt_SamplingRate: Int_EndSec*Flt_SamplingRate]

    if PLOT:
        plt.figure()
        plt.title("PPG")
        plt.grid()
        plt.plot(Array_Time, Array_PPG,label = "Raw PPG")
        plt.legend()
        plt.show()
