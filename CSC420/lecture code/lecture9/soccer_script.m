function soccer_script(annotate_pts)
% by Sanja Fidler, UofT
% annotate_pts ... 0 or 1 depending if you want to annotate the points
% yourself

if nargin < 1
    annotate_pts = 0;
end;
im = imread('soccer_field.jpg');

if annotate_pts
   imshow(im);
   disp('click on the four corners of the field. Double click the last point');
   [x,y] = getpts();
   close all;
   imshow(im);
   disp('now click the points of a player''s trajectory');
   [xt,yt] = getpts();
else
    x = [418.2500, 914.7500, 455.7500, 70.2500]';
    y = [149.5000, 244.0000, 391.0000, 185.5000]';
    xt = [518.7500, 484.2500, 413.7500, 440.7500, 406.2500, 341.7500]';
    yt = [251.5000  251.5000  244.0000  200.5000  184.0000  179.5000]';
end;

% display the image and picked points
figure('position', [100,100,size(im,2),size(im,1)]);
subplot('position', [0,0,1,1]);
imshow(im);
hold on;
plot([x(:); x(1)],[y(:); y(1)],'-o','linewidth',2,'color', [1,0.1,0.1], 'Markersize',10,'markeredgecolor',[0,0,0],'markerfacecolor',[0.5,0.0,1])
plot(xt(:),yt(:),'-o','linewidth',2,'color', [0,0.3,1], 'Markersize',10,'markeredgecolor',[0,0,0],'markerfacecolor',[1,0,0])

% get dimensions of a soccer field and put in matrix
f=20; % each meter is f pixels
x2=[0,55*f,55*f,0]'+1;
y2=[0,0,36.6*f,36.6*f]'+1;

% compute homography
tform = maketform('projective',[x,y],[x2,y2]);

% warp the image according to homography
[imrec] = imtransform(im, tform, 'bicubic',...
    'xdata', [1,f*55],...
    'ydata', [1,f*36.6],...
    'size', [f*36.6, f*55],...
    'fill', 0);
figure('position', [150,150,size(imrec,2)*0.7,size(imrec,1)*0.7]);
subplot('position', [0,0,1,1]);
imshow(imrec)
hold on;

% transform the trajectory
X_hom=tform.tdata.T'*[xt';yt';ones(1,length(xt))];  % be careful, Matlab has the matrix transposed

X_hom=X_hom./repmat(X_hom(3,:),[3,1]);
plot(X_hom(1,:)',X_hom(2,:)','-o','linewidth',2,'color', [0,0.3,1], 'Markersize',10,'markeredgecolor',[0,0,0],'markerfacecolor',[1,0,0])
end