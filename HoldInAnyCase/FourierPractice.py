import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
import pylab as plt

time   = np.linspace(0,1,500)
signal = np.cos(5*np.pi*time) + np.cos(7*np.pi*time)

W = fftfreq(signal.size, d=time[1]-time[0])
print W
f_signal = rfft(signal)

# If our original signal time was in seconds, this is now in Hz
cut_f_signal = f_signal.copy()
cut_f_signal[(W<6)] = 0

cut_signal = irfft(cut_f_signal)

plt.subplot(221)
plt.plot(time,signal)
plt.subplot(222)
plt.stem(W,f_signal)
plt.xlim(0,10)
plt.subplot(223)
plt.stem(W,cut_f_signal)
plt.xlim(0,10)
plt.subplot(224)
plt.plot(time,cut_signal)
plt.show()
