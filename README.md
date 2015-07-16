# PPG_Reexperiment
## Goal 
Develop real-time algorithm for detecting peaks of PPG.

## Folder Description 
#### Module 
- AdaptiveThreshold 
  - Adaptive Threshold suggested by Shin et al., 2009 
- bandpass 
  - Band Pass Filter 
- FourierTransformation 
  - Conducting FFT, IFFT (Inverse FFT) 
- LMSFilter 
  - Conduct LMS filter algorithm to obtain MA-reduced PPG signal 
- SlopeSumFunction 
  - Conduct Slope sum for enhancing up-slope of PPG, suggested by Jang et al., 2014 

#### CompetitingMethod
- CompeteteMethod_FirstDeriv
  - PPG peak detection method based on First Derivative based method, suggested by Li et al., (2010)
- CompeteteMethod_LCM
  - PPG peak detection method based on Local Maxima based method, suggested by Domingues et al., (2009)
- CompeteteMethod_SSF
  - PPG peak detection method based on Local Maxima based method, suggested by Jang et al., (2014)

#### Execution 
- Execution.py : Main file 

