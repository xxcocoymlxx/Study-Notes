function out = smoothImage(im)
% smooths image with Gaussian kernel
% by Sanja Fidler, UofT

im = double(im);

sigmas = [2, 5, 20];

% let's see how blurs with different sigmas look like
out = cell(length(sigmas), 1);
for i = 1 : length(sigmas)
   sigma = sigmas(i);
   % note that a Gaussian function is defined everywhere in R^2
   % -> but filter is finite
   % -> we need to decide on the size of the filter
   % 2 times sigma gets 99.8% of variance
   % (if that's not enough, use factor 5 which gives 99.99999% of variance
   % read about here: http://en.wikipedia.org/wiki/Normal_distribution
   filter_size = 3 * sigma;
   f = fspecial('gaussian', [filter_size, filter_size], sigma);  % create the filter
   out_i = zeros(size(im));
   for j = 1 : size(im, 3)  % let's smooth each color channel
      out_i(:,:,j) = filter2(f, im(:,:,j));
   end;
   out{i} = out_i;
end;

% let's plot it all

% make a nice plot
f = 0.5;  % scale down plot a bit
w = size(im, 2) * (length(sigmas)+1) * f; % width of the plot
h = f * size(im, 1);  % height of the plot
figure('position', [100,100, w, h + 30]);
subplot('position', [0,0,1/(length(sigmas)+1), h / (h+30)]);
uicontrol('style','text','string','image','position',[size(im, 2) * f/2,  h + 8, 60, 20],'fontsize',18, 'BackgroundColor', [0,0,0], 'ForegroundColor', [1,0.2,0.2]); 

imshow(uint8(im))
for i = 1:length(sigmas)
    subplot('position', [i * 1 / (length(sigmas)+1),0,1/(length(sigmas)+1), h / (h+30)]);
    imshow(uint8(out{i}))
    uicontrol('style','text','string',sprintf('sigma: %0.2f', sigmas(i)),'position',[(i + 0.5) * w/(length(sigmas)+1) - 120/2,  h + 8, 120, 20],'fontsize',18, 'BackgroundColor', [0,0,0], 'ForegroundColor', [1,0.2,0.2]);
end;
set(gcf, 'Color', [0,0,0])

end

