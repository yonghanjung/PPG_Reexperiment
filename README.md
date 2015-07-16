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

#### Execution 
- Execution.py : Main file 
