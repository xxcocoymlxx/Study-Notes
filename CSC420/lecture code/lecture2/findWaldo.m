function out = findWaldo(im, filter)
% returns the output of normalized cross-correlation between image im and filter 
% by Sanja Fidler, UofT

% convert image (and filter) to grayscale
im_input = im;
im = rgb2gray(im);
im = double(im);
filter = rgb2gray(filter);
filter = double(filter);
filter = filter/sqrt(sum(sum(filter.^2)));

% normalized cross-correlation
out = normxcorr2(filter, im);

% plot the cross-correlation results
figure('position', [100,100,size(out,2),size(out,1)]);
subplot('position',[0,0,1,1]);
imagesc(out)
axis off;
axis equal;

% find the peak in response
[y,x] = find(out == max(out(:)));
y = y(1) - size(filter, 1) + 1;
x = x(1) - size(filter, 2) + 1;

% plot the detection's bounding box
figure('position', [300,100,size(im,2),size(im,1)]);
subplot('position',[0,0,1,1]);
imshow(im_input)
axis off;
axis equal;
rectangle('position', [x,y,size(filter,2),size(filter,1)], 'edgecolor', [0.1,0.2,1], 'linewidth', 3.5);

end