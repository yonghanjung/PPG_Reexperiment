import scipy.io
import numpy as np
import matplotlib.pyplot as plt
B = open("212_Anno.txt",'rb')

Idx = []

for b in B.readlines() :
    AA = b.split(" ")
    BB = [elem for elem in AA if elem != ""]
    try:
        PeakIdx = int(BB[2])
        Idx.append(PeakIdx)
    except:
        pass

print Idx

A = scipy.io.loadmat("212m.mat")['val']
A = np.squeeze(np.asarray(A))
Domain = np.linspace(0,len(A), len(A))
Idx = np.array(Idx)
plt.plot(Domain, A)
plt.plot(Idx, A[Idx],'ro')
plt.show()
