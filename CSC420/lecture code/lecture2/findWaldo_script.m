im = imread('clutter.png');
filter = imread('waldo.png');

output = findWaldo(im, filter);