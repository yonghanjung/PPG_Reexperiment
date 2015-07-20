import scipy.io
import numpy as np
import matplotlib.pyplot as plt

StrDataName = "../Data/SLP/slp01am"
MatFile_Data = scipy.io.loadmat(StrDataName)['val']
MatFile_Data = np.squeeze(np.asarray(MatFile_Data))
MatFile_Data = MatFile_Data[:1000]
print len(MatFile_Data)

plt.plot(MatFile_Data)
plt.plot(687, MatFile_Data[687],'ro')
plt.show()

