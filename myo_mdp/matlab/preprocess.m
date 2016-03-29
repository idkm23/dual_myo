function [data, emg, imu] = preprocess(dataPath)
% Data preprocessing

EMG = csvread(strcat(dataPath,'emg.mat'));
ACC = csvread(strcat(dataPath, 'acceleration.mat'));
GYRO = csvread(strcat(dataPath, 'gyro.mat'));
ORI = csvread(strcat(dataPath, 'orientation.mat'));

IMU = [ACC, GYRO, ORI];
clear ACC;
clear GYRO;
clear ORI;

% downsampling, trashing the first and last 5 points
EMG = EMG(6:5:end-5, :);
IMU = IMU(6:5:end-5, :);

n = size(EMG, 1); % usually there are slightly fewer points in EMG data
fprintf('difference: %d \n',size(IMU, 1)-n);
IMU = IMU(1:n, :);

% handled the -180/+180 issue
% maybe we need a probablistic model in the future.
IMU(:,7) = abs(IMU(:,7));

% put data together
Data = [EMG,IMU];
Data = sgolayfilt(Data,3,41);

% add time dimension
Data = [[1:n]', Data];

% normalize data
[data, emg, acc, gyro, orie] = normalize_myo(Data);
imu = [acc, gyro, orie];

% change to row vectors
%Data = [1:n; Data'];

end
