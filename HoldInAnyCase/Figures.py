import matplotlib.pyplot as plt
import numpy as np
from Module.data_call import data_call
import matplotlib



Int_SampRate = 75
Int_StartSec = 10
Int_EndSec = 13

# No MA
Str_DataName_NoMA = "PPG_KW_long"
Int_DataNum_NoMA = 2

# Weak MA
Str_DataName_WMA = "PPG_Walk"
Int_DataNum_WMA = 3

# Strong MA
Str_DataName_SMA = "PPG_Walk"
Int_DataNum_SMA = 2
Int_CutMin = Int_SampRate * 60

Array_PPGData_NoMA = data_call(data_name=Str_DataName_NoMA, data_num=Int_DataNum_NoMA, wanted_length=0)[:Int_CutMin]
Array_PPGData_WMA = data_call(data_name=Str_DataName_WMA, data_num=Int_DataNum_WMA, wanted_length=0)[:Int_CutMin]
Array_PPGData_SMA = data_call(data_name=Str_DataName_SMA, data_num=Int_DataNum_SMA, wanted_length=0)[:Int_CutMin]
Array_Time = np.linspace(0, len(Array_PPGData_NoMA)/Int_SampRate, len(Array_PPGData_NoMA))

# PLOT
matplotlib.rcParams.update({'font.size': 15})
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1.plot(Array_Time, Array_PPGData_NoMA)
ax2.plot(Array_Time, Array_PPGData_WMA)
ax3.plot(Array_Time, Array_PPGData_SMA)
plt.xlabel("Time (Sec)", fontsize=20)

plt.show()



