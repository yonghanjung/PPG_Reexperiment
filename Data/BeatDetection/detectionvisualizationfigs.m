% Script to visualize annotations

%===========================================================
% ICP
%=========================================================== 
load ICP;

% ICP1
figure
%figureset(1,'wide');
fs = 125;
t  = (1:length(icp1))./fs;
h  = plot(t, icp1, d1./fs, icp1(d1), 'k+', ...
    dDT1./fs, icp1(dDT1), 'r.', ...
    dJM1./fs, icp1(dJM1), 'gx');
set(h, 'Markersize', 12);
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset(8);

% ICP2
figure
%figureset(3,'wide');
fs = 125;
t  = (1:length(icp2))./fs;
h  = plot(t, icp2, d2./fs, icp2(d2), 'k+', ...
    dDT2./fs, icp2(dDT2), 'r.', ...
    dJM2./fs, icp2(dJM2), 'gx');
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
set(h, 'Markersize', 12);
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset(8);


%===========================================================
% ABP
%=========================================================== 
load abp;

% abp1
figure
%figureset(1,'wide');
fs = 125;
t  = (1:length(abp1))./fs;
h  = plot(t, abp1, d1./fs, abp1(d1), 'k+', ...
    dDT1./fs, abp1(dDT1), 'r.', ...
    dJM1./fs, abp1(dJM1), 'gx');
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
set(h, 'Markersize', 12);
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset(8);

% abp2
figure
%figureset(3,'wide');
fs = 125;
t  = (1:length(abp2))./fs;
h  = plot(t, abp2, d2./fs, abp2(d2), 'k+', ...
    dDT2./fs, abp2(dDT2), 'r.', ...
    dJM2./fs, abp2(dJM2), 'gx');
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
set(h, 'Markersize', 12);
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset(8);


%===========================================================
% pox
%=========================================================== 
load pox;

% pox1
figure
%figureset(1,'wide');
fs = 125;
t  = (1:length(pox1))./fs;
h  = plot(t, pox1, d1./fs, pox1(d1), 'k+', ...
    dDT1./fs, pox1(dDT1), 'r.', ...
    dJM1./fs, pox1(dJM1), 'gx');
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
set(h, 'Markersize', 12);
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset(8);

% pox2
figure
%figureset(3,'wide');
fs = 125;
t  = (1:length(pox2))./fs;
h  = plot(t, pox2, d2./fs, pox2(d2), 'k+', ...
    dDT2./fs, pox2(dDT2), 'r.', ...
    dJM2./fs, pox2(dJM2), 'gx');
legend('Raw Signal', 'Detector', 'Expert-1 (DT)', 'Expert-2 (JM)');
set(h, 'Markersize', 12);
xlabel('Time, s');
ylabel('Signal & Detection');
box off; 
%axisset;(8)