import scipy.io
import numpy as np
import matplotlib.pyplot as plt

Str_DataPathABP = "../Data/BeatDetection/ABP"
Str_DataPathICP = "../Data/BeatDetection/ICP"
MatFile_ABP = scipy.io.loadmat(Str_DataPathABP)
MatFile_ICP = scipy.io.loadmat(Str_DataPathICP)

Array_PPG1 = np.array(MatFile_ICP['icp1'])
Array_PPG2 = np.array(MatFile_ICP['icp2'])
Array_TimeDomain1 = np.linspace(0, len(Array_PPG1)/125.0, len(Array_PPG1))
Array_TimeDomain2 = np.linspace(0, len(Array_PPG2)/125.0, len(Array_PPG2))

Array_Peak1_Expert1 = np.squeeze(np.array(MatFile_ICP['dDT1']))
Array_Peak1_Expert2 = np.squeeze(np.array(MatFile_ICP['dJM1']))
Array_Peak1_Expert3 = np.squeeze(np.array(MatFile_ICP['dTT1']))

Array_Peak2_Expert1 = np.squeeze(np.array(MatFile_ICP['dDT2']))
Array_Peak2_Expert2 = np.squeeze(np.array(MatFile_ICP['dJM2']))
Array_Peak2_Expert3 = np.squeeze(np.array(MatFile_ICP['dTT2']))

Int_Cut = 125 * 60
Array_PPG1 = Array_PPG1[:Int_Cut]
Array_TimeDomain1 = Array_TimeDomain1[:Int_Cut]
Array_Peak1_Expert1 = np.array([int(val) for val in Array_Peak1_Expert1 if val < Int_Cut])


plt.plot(Array_TimeDomain1, Array_PPG1)
plt.plot(Array_TimeDomain1[Array_Peak1_Expert1], Array_PPG1[Array_Peak1_Expert1], 'ro')
plt.show()

