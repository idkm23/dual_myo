function [Data, EMG, ACC, GYRO, ORIE] = normalize_myo(data)
% every column of data is a time series
% every row is a data point

T = data(:,1);
EMG = data(:,2:9);
ACC = data(:,10:12);
GYRO = data(:,13:15);
ORIE = data(:,16:18);

%EMG_max = max(max(EMG));
%EMG_min = min(min(EMG));
EMG_max = 585.38
EMG_min = 32.033
EMG = (EMG-EMG_min)/(EMG_max-EMG_min+1);


% ACC = ACC - repmat(mean(ACC(1:3,:)), size(ACC,1),1);

% GYRO is directional, can be pos or neg
% but the absolute values are about symmetric
%GYRO_max = max(max(GYRO));
GYRO_max = 500
GYRO = GYRO/GYRO_max;


% range is -180~180 degrees
ORIE = ORIE/180;

Data = [T,EMG,ACC,GYRO,ORIE];

end
