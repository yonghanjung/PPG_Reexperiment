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
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

''' Function or Class '''


class LowPassFilter:
    def __init__(self, Array_Signal, Flt_CutOffFreq, Flt_SamplingRate):
        self.Array_Signal = Array_Signal
        self.Flt_CutOffFreq = Flt_CutOffFreq
        self.Int_Order = 5
        self.Flt_SamplingRate = Flt_SamplingRate

    def butter_lowpass(self):
        Flt_nyqFreq = 0.5 * self.Flt_SamplingRate
        normal_cutoff = self.Flt_CutOffFreq / Flt_nyqFreq
        b, a = butter(self.Int_Order, normal_cutoff, btype='low', analog=False)
        return b, a

    def LowPassFilter(self):
        b, a = self.butter_lowpass()
        y = lfilter(b, a, self.Array_Signal)
        return y

#
# # Filter requirements.
# order = 6
# fs = 30.0       # sample rate, Hz
# cutoff = 3.667  # desired cutoff frequency of the filter, Hz
#
# # Get the filter coefficients so we can check its frequency response.
# b, a = butter_lowpass(cutoff, fs, order)
#
# # Plot the frequency response.
# w, h = freqz(b, a, worN=8000)
# plt.subplot(2, 1, 1)
# plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
# plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
# plt.axvline(cutoff, color='k')
# plt.xlim(0, 0.5*fs)
# plt.title("Lowpass Filter Frequency Response")
# plt.xlabel('Frequency [Hz]')
# plt.grid()
#
#
# # Demonstrate the use of the filter.
# # First make some data to be filtered.
# T = 5.0         # seconds
# n = int(T * fs) # total number of samples
# t = np.linspace(0, T, n, endpoint=False)
# # "Noisy" data.  We want to recover the 1.2 Hz signal from this.
# data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)
#
# # Filter the data, and plot both the original and filtered signals.
# y = butter_lowpass_filter(data, cutoff, fs, order)
#
# plt.subplot(2, 1, 2)
# plt.plot(t, data, 'b-', label='data')
# plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
# plt.xlabel('Time [sec]')
# plt.grid()
# plt.legend()
#
# plt.subplots_adjust(hspace=0.35)
# plt.show()