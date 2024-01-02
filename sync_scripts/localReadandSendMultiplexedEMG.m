function localReadandSendMultiplexedEMG(interfaceObjectEMG, ~)

global rateAdjustedEmgBytesToRead;
global NUM_SENSORS;

bytesReady = interfaceObjectEMG.BytesAvailable;
bytesReady = bytesReady - mod(bytesReady, rateAdjustedEmgBytesToRead);%%1728 and 0 if multiple of this

if (bytesReady == 0)
    return
end

global data_arrayEMG
data = cast(fread(interfaceObjectEMG,bytesReady), 'uint8');
data = typecast(data, 'single');

data_ = reshape(data,16,length(data)/16);
dat_lsl = data_(1:NUM_SENSORS,:);
global outlet
outlet.push_chunk(double(dat_lsl));



if(size(data_arrayEMG, 1) < rateAdjustedEmgBytesToRead)
    data_arrayEMG = [data_arrayEMG; data];
end
end
