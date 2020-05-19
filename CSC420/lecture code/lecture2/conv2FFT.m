function g = conv2FFT(h, im)

% g = conv2FFT(h, f)
%
% DESC:
% computes the 2D convolution via FFT
%
% AUTHOR
% Marco Zuliani - zuliani@ece.ucsb.edu
%
% VERSION:
% 1.0.0
%
% INPUT:
% h                 = convolution kernel
% f                 = input signal
%
% OUTPUT:
% g                 = output signal
%
% HISTORY
% 1.0.0             ??/??/07 Initial version

sh = size(h);
sf = size(im);

% zero pad the input signals
fm = zeros(sf+2*(sh-1), class(im));
o = sh-1;
fm( o(1)+(1:size(im,1)), o(2)+(1:size(im,2)) ) = im;

h_zp = zeros(size(fm), class(h));
h_zp(1:size(h,1), 1:size(h,2)) = h;

% compute the convolution in frequency
F = fft2(fm);
H = fft2(h_zp);
Y = F.*H;

% back to spatial domain
g = real( ifft2(Y) );

% remove padding
o = floor(1.5*size(h))-1;
g = g( o(1)+(1:size(im,1)), o(2)+(1:size(im,2)) );

return