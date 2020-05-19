function out = harriscorner(filename)
% read image and grayscale
im = imread(filename);

% convert to grayscale
img = rgb2gray(im);

%get dimensions
[img_height, img_width] = size(img);

% get image gradients Ix and Iy
[Ix, Iy] = imgradientxy(img);

% compute 3 matrixes Ix^2, Iy^2, Ix * Iy
Ix2 = Ix.^2;
Iy2 = Iy.^2;
Ixy = Ix.*Iy;

% compute matrix M = [Ix2g, Ixyg; Ixyg, Iy2g];
% convolving each one with a filter, e.g. a box or Gaussian filter
Ix2g = conv2(Ix2, fspecial('gaussian'), 'same');
Iy2g = conv2(Iy2, fspecial('gaussian'), 'same');
Ixyg = conv2(Ixy, fspecial('gaussian'), 'same');

% compute R = det(M) - alpha*trace(M)^2
alpha = 0.04; % a constance

Rmax = 0;
R = zeros(img_height, img_width);

det_M = Ix2g.*Iy2g - Ixyg.^2;
trace_M = Ix2g + Iy2g; 

R = det_M - alpha*((trace_M).^2);
Rmax = max(max(R));

% Non-maximum suppression
Res = zeros(img_height, img_width);
thresh = Rmax*0.028;

for row = 1:img_height
    for col = 1:img_width
        % check for local max
        if R(row,col) > thresh
            local_max = true;
            for n = row-1:row+1
                for m = col-1:col+1
                    if R(n, m) > R(row, col)
                        local_max = false;
                        break
                    end
                end
                if local_max == false
                    break
                end
            end
            if local_max == true
                Res(row,col) = 1;
            end
        end
    end
end

[cols, rows] = find(Res == 1);
imshow(img);
hold on;
plot(rows,cols,'r.');
end