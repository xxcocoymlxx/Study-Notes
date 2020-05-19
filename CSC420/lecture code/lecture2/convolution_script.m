im = imread('clutter.png');
im = double(rgb2gray(im));
filter = fspecial('disk', 10);
fprintf('filter size: %d\n', size(filter, 1));
compareConvolutionMethods(im, filter)

disp('-------------');
filter = fspecial('disk', 60);
fprintf('filter size: %d\n', size(filter, 1));
compareConvolutionMethods(im, filter)