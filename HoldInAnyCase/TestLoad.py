import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from Module.data_call import data_call

# StrDataName = "../Data/SLP/slp01am"
# MatFile_Data = scipy.io.loadmat(StrDataName)['val']
# MatFile_Data = np.squeeze(np.asarray(MatFile_Data))
# MatFile_Data = MatFile_Data[:1000]
# print len(MatFile_Data)
#
# plt.plot(MatFile_Data)
# plt.plot(687, MatFile_Data[687],'ro')
# plt.show()
#

# Str_DataName = "PPG_Walk"
Str_DataName = "PPG_KW_long"
Int_DataNum = 0
Int_SampRate = 75

Array_PPGData = data_call(data_name=Str_DataName, data_num=Int_DataNum, wanted_length=0)
Array_Time = np.linspace(0, len(Array_PPGData)/Int_SampRate, len(Array_PPGData))
# print len(Array_PPGData) / Int_SampRate



matplotlib.rcParams.update({'font.size': 23})
plt.plot(Array_Time, Array_PPGData)
plt.xlabel("Time (sec)", fontsize = 30)
plt.ylabel("Voltage", fontsize=30)
plt.show()


# Str_DataPathABP = "../Data/BeatDetection/ABP"
# Str_DataPathICP = "../Data/BeatDetection/ICP"
# MatFile_ABP = scipy.io.loadmat(Str_DataPathABP)
# MatFile_ICP = scipy.io.loadmat(Str_DataPathICP)
#
# Array_PPG1 = np.array(MatFile_ABP['abp1'])
# Array_PPG2 = np.array(MatFile_ABP['abp2'])
# Array_TimeDomain1 = np.linspace(0, len(Array_PPG1)/125.0, len(Array_PPG1))
# Array_TimeDomain2 = np.linspace(0, len(Array_PPG2)/125.0, len(Array_PPG2))
#
# Array_Peak1_Expert1 = np.squeeze(np.array(MatFile_ICP['dDT1']))
# Array_Peak1_Expert2 = np.squeeze(np.array(MatFile_ICP['dJM1']))
# Array_Peak1_Expert3 = np.squeeze(np.array(MatFile_ICP['dTT1']))
#
# Array_Peak2_Expert1 = np.squeeze(np.array(MatFile_ICP['dDT2']))
# Array_Peak2_Expert2 = np.squeeze(np.array(MatFile_ICP['dJM2']))
# Array_Peak2_Expert3 = np.squeeze(np.array(MatFile_ICP['dTT2']))
#
# Int_Cut = 125 * 60
# Array_PPG1 = Array_PPG1[:Int_Cut]
# Array_TimeDomain1 = Array_TimeDomain1[:Int_Cut]
# Array_Peak1_Expert1 = np.array([int(val) for val in Array_Peak1_Expert1 if val < Int_Cut])
#
# print MatFile_ABP.keys()

# plt.plot(Array_TimeDomain1, Array_PPG1)
# plt.plot(Array_TimeDomain1[Array_Peak1_Expert1], Array_PPG1[Array_Peak1_Expert1], 'ro')
# plt.show()



