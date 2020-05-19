
%get the result
output = q3b(im, filter);


function out = q3b(im, template)

% convert image (and filter) to grayscale
im_input = im;
im = rgb2gray(im);
im = double(im);
template = rgb2gray(template);
template = double(template);
template = template/sqrt(sum(sum(template.^2)));

%Assume the gradient of each image was correctly return by the function in Q3(a)
G_im, D_im = magnitude_of_gradients(im);
G_temp, D_temp = magnitude_of_gradients(template);
% normalized cross-correlation
out = normxcorr2(G_temp, G_im);

% plot the cross-correlation results
figure('position', [100,100,size(out,2),size(out,1)]);
subplot('position',[0,0,1,1]);
imagesc(out)
axis off;
axis equal;

% find the peak in response
[y,x] = find(out == max(out(:)));
y = y(1) - size(template, 1) + 1;
x = x(1) - size(template, 2) + 1;

% plot the detection's bounding box
figure('position', [300,100,size(im,2),size(im,1)]);
subplot('position',[0,0,1,1]);
imshow(G_im, []);
imshow(im_input);
axis off;
axis equal;
rectangle('position', [x,y,size(template,2),size(template,1)], 'edgecolor', [0.1,0.2,1], 'linewidth', 3.5);

end