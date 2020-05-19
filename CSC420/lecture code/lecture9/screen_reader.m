function screen_reader(annotate_pts)
% by Sanja Fidler, UofT
% annotate_pts ... 0 or 1 depending if you want to annotate the points
% yourself

if nargin < 1
    annotate_pts = 0;
end;
im = imread('cheating.jpeg');

if annotate_pts
   imshow(im);
   disp('click on the four corners of the screen. Double click the last point');
   [x,y] = getpts();
   close all;
   imshow(im);
else
   x = [1012.8535 1388.0473 1451.0798 1093.8953]';
   y = [326.1682 485.2504 1334.6891 926.4783]';
end;

% display the image and picked points
figure('position', [100,100,size(im,2)*0.3,size(im,1)*0.3]);
subplot('position', [0,0,1,1]);
imshow(im);
hold on;
plot([x(:); x(1)],[y(:); y(1)],'-o','linewidth',2,'color', [1,0.1,0.1], 'Markersize',10,'markeredgecolor',[0,0,0],'markerfacecolor',[0.5,0.0,1])

x2 = [1, 1440, 1440, 1]';
y2 = [1, 1, 900, 900]';

% compute homography
tform = maketform('projective',[x,y],[x2,y2]);

% warp the image according to homography
[imrec] = imtransform(im, tform, 'bicubic',...
    'xdata', [1,max(x2)],...
    'ydata', [1,max(y2)],...
    'size', [max(y2), max(x2)],...
    'fill', 0);
figure('position', [150,150,size(imrec,2)*0.6,size(imrec,1)*0.6]);
subplot('position', [0,0,1,1]);
imshow(imrec)
end