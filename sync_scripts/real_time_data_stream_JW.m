%% RealTime Data Streaming with Delsys SDK to LSL
% 
% Software to plot Delsys Quattro EMG and send data to the Lab Streaming
% Layer protocol

% Author:   Julius Welzel, j.welzel@neurologie.uni-kiel.de
% Repo:     github.com/JuliusWelzel/int_trmr_eeg
% Based on real_time_data_plotting as MatLab example by Trigno SDK
% Version   0.2.0 // 08.12.2023


% CHANGE THIS TO THE IP OF THE COMPUTER RUNNING THE TRIGNO CONTROL UTILITY
HOST_IP = 'localhost';
%%
%This example program communicates with the Delsys SDK to stream 16
%channels of EMG data.



%% Create the required objects

%Define number of sensors (one Avanti)
global  NUM_SENSORS
NUM_SENSORS = 5;
global rateAdjustedEmgBytesToRead;
rateAdjustedEmgBytesToRead=6400;
global data_arrayEMG
data_arrayEMG = [];


%TCPIP Connection to stream EMG Data
interfaceObjectEMG = tcpip(HOST_IP,50043);
interfaceObjectEMG.InputBufferSize = rateAdjustedEmgBytesToRead * 5;


%TCPIP Connection to communicate with SDK, send/receive commands
commObject = tcpip(HOST_IP,50040);


%%Open the COM interface, determine RATE
fopen(commObject);

%% setup LSL
% instantiate LSL
lib = lsl_loadlib();

% make a new stream outlet
info = lsl_streaminfo(lib,'Delsys','EMG',NUM_SENSORS,rateAdjustedEmgBytesToRead,'cf_double64');
global outlet
outlet = lsl_outlet(info); 

display('LSL outlet created');

input('Start LabRecorder')
%% Setup interface object to read chunks of data
% Define a callback function to be executed when desired number of bytes
% are available in the input buffer
 bytesToReadEMG = rateAdjustedEmgBytesToRead;
 interfaceObjectEMG.BytesAvailableFcn = {@localReadandSendMultiplexedEMG,bytesToReadEMG};
 interfaceObjectEMG.BytesAvailableFcnMode = 'byte';
 interfaceObjectEMG.BytesAvailableFcnCount = bytesToReadEMG;
 

%pause(1);
%% Open the interface object 

% now really open interface
fopen(interfaceObjectEMG);
display('Opened connections');



%%
% Send the commands to start data streaming
fprintf(commObject, sprintf(['START\r\n\r']));

fprintf(commObject, sprintf(['STOP\r\n\r']));


