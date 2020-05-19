im = imread('waldo.png');
img = rgb2grey(im);
canny = edge(img, 'canny', [0,0.50]);
imshow(canny);