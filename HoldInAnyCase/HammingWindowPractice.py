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
import matplotlib.pyplot as plt
from Execution.Execution import DrMPPGAnalysis
''' Function or Class '''


class Example:
    def __init__(self):
        return None


if __name__ == "__main__":
    T = np.linspace(0,10, 100)
    Freq1 = 3
    Freq2 = 5
    Y = np.cos(2*np.pi * Freq1 * T) + np.sin(2*np.pi* Freq2 * T)
    HammingWindow = np.hamming(len(T))
    YHAT = Y * HammingWindow

    plt.figure()
    plt.grid()
    plt.plot(T,Y,'b')
    plt.plot(T,YHAT,'g')
    plt.show()
