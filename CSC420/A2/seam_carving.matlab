function out = seam_carving(image)

% read image and convert to grayscale
im = imread(image);
[rows, cols, dim] = size(im);
img = rgb2gray(im);

% compute gradients
[Gx, Gy] = imgradientxy(img);
Gmag = sqrt(Gx.^2 + Gy.^2);
[row_g, col_g, ~] = size(Gmag);
seam_img(1,:) = Gmag(1,:);
seam_img = zeros(row_g, col_g);

% calculate horizontal seam
for col = 2:rows
    for row = 1:rows
        if (row == 1)
            min_energy = min([seam_img(row, col - 1), seam_img(row + 1, col-1)]);
        elseif (row == rows)
            min_energy = min([seam_img(row - 1, col - 1), seam_img(row, col - 1)]);
        else
            min_energy = min([seam_img(row - 1, col - 1), seam_img(row,col - 1), seam_img(row + 1, col - 1)]);
        end
        seam_img(row, col) = Gmag(row, col) + min_energy;
    end
end

seam_img = Gmag;

% calculate min value 
[val, index] = min(seam_img(:, cols));
seam = zeros(cols, 1);
seam(cols) = index;

while cols > 1
    cols = cols - 1;
    min_val = seam_img(index, cols);
    i = index;
    
    if index ~= 1
        if seam_img(index - 1, cols) < min_val
            min_val = seam_img(index - 1, cols);
            i = index - 1;
        end
    end

    if index ~= cols
        if seam_img(index + 1, cols) < min_val
            i = index + 1;
        end 
    end
    
    seam(cols) = i;
    index = i;
end

% remove seam
% for dim = 1:3
%     for col = 1:cols
%         for row = seam(col):rows - 1
%             im(row, col, dim) = im(row + 1, col, dim);
%         end
%     end
% end
% removed_output = im(1:rows - 1, :, :);
% 
% im = removed_output;

% show seam
for i = 1:size(seam, 1)
    im(seam(i), i, 1:3) = 0;
end

imshow(im);