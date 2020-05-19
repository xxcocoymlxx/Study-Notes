function compareConvolutionMethods(im, filter)
% compares convolution with matlab's conv2 (slides a filter) and FFT

tic;
gFFT = conv2FFT(filter, im);
time_fft = toc;

tic;
% try both functions!
%gConv = conv2(im, filter, 'same');
gConv = imfilter(im, filter, 'same', 'conv'); % matlab's convolution is really optimized
time_conv = toc;

fprintf('Time for sliding convolution: %0.4f\n', time_conv);
fprintf('Time for convolution via FFT: %0.4f\n', time_fft);

if 0
figure('position', [100,100,size(im, 2) * 3, size(im, 1)])
subplot('position', [0,0,1/3,1]);
imagesc(gConv);
subplot('position', [1/3,0,1/3,1]);
imagesc(gFFT);
subplot('position', [2/3,0,1/3,1]);
gFFT = gFFT / max(gFFT(:));
gConv = gConv / max(gConv(:));
imagesc(abs(gFFT - gConv), [0,1]);

fprintf('plot from left to right: sliding conv, conv via FFT, difference\n')
fprintf('blue color is 0, red is 1\n')
end;

end