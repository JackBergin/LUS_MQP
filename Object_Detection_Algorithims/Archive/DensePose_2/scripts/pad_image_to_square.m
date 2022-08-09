%%
clc; clear; close all

filepath = '../DensePoseData/image_buffer/Randy-supine.jpg';
I = imread(filepath);

if size(I,1) ~= size(I,2)
    [~, dim2pad] = min(size(I,1:2));
    pad_width = max(size(I,1:2)) - min(size(I,1:2));
    I_padded = zeros(max(size(I,1:2)),max(size(I,1:2)),3,'uint8');
    if dim2pad == 1
        I_padded(pad_width/2:pad_width/2+size(I,1)-1,:,:) = I;
    elseif dim2pad == 2
        I_padded(:,pad_width/2:pad_width/2+size(I,2)-1,:) = I;
    end
else
    I_padded = I;
end

% I_padded = imrotate(I_padded, 90);
imshow(I_padded)
imwrite(I_padded,filepath)
