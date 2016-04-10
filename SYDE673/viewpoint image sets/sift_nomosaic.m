function mosaic = sift_mosaic(im1, im2)
% SIFT_MOSAIC Demonstrates matching two images using SIFT and RANSAC
%
%   SIFT_MOSAIC demonstrates matching two images based on SIFT
%   features and RANSAC and computing their mosaic.
%
%   SIFT_MOSAIC by itself runs the algorithm on two standard test
%   images. Use SIFT_MOSAIC(IM1,IM2) to compute the mosaic of two
%   custom images IM1 and IM2.

% AUTORIGHTS

if nargin == 0
  im1 = imread(fullfile(vl_root, 'data', 'river1.jpg')) ;
  im2 = imread(fullfile(vl_root, 'data', 'river2.jpg')) ;
else
  im1 = imread(im1) ;
  im2 = imread(im2) ;    
end

% make single
im1 = im2single(im1) ;
im2 = im2single(im2) ;

% make grayscale
if size(im1,3) > 1, im1g = rgb2gray(im1) ; else im1g = im1 ; end
if size(im2,3) > 1, im2g = rgb2gray(im2) ; else im2g = im2 ; end

% --------------------------------------------------------------------
%                                                         SIFT matches
% --------------------------------------------------------------------

[f1,d1] = vl_sift(im1g) ;
[f2,d2] = vl_sift(im2g) ;

[matches, scores] = vl_ubcmatch(d1,d2) ;

numMatches = size(matches,2) ;

X1 = f1(1:2,matches(1,:)) ; X1(3,:) = 1 ;
X2 = f2(1:2,matches(2,:)) ; X2(3,:) = 1 ;

% --------------------------------------------------------------------
%                                         RANSAC with homography model
% --------------------------------------------------------------------

clear H score ok ;
for t = 1:100
  % estimate homograpyh
  subset = vl_colsubset(1:numMatches, 4) ;
  A = [] ;
  for i = subset
    A = cat(1, A, kron(X1(:,i)', vl_hat(X2(:,i)))) ;
  end
  [U,S,V] = svd(A) ;
  H{t} = reshape(V(:,9),3,3) ;

  % score homography
  X2_ = H{t} * X1 ;
  du = X2_(1,:)./X2_(3,:) - X2(1,:)./X2(3,:) ;
  dv = X2_(2,:)./X2_(3,:) - X2(2,:)./X2(3,:) ;
  ok{t} = (du.*du + dv.*dv) < 6*6 ;
  score(t) = sum(ok{t}) ;
end

[score, best] = max(score) ;
H = H{best} ;
ok = ok{best} ;
H

% --------------------------------------------------------------------
%                                                  Optional refinement
% --------------------------------------------------------------------

function err = residual(H)
 u = H(1) * X1(1,ok) + H(4) * X1(2,ok) + H(7) ;
 v = H(2) * X1(1,ok) + H(5) * X1(2,ok) + H(8) ;
 d = H(3) * X1(1,ok) + H(6) * X1(2,ok) + 1 ;
 du = X2(1,ok) - u ./ d ;
 dv = X2(2,ok) - v ./ d ;
 err = sum(du.*du + dv.*dv) ;
end

if exist('fminsearch') == 2
  H = H / H(3,3) ;
  opts = optimset('Display', 'none', 'TolFun', 1e-8, 'TolX', 1e-8) ;
  H(1:8) = fminsearch(@residual, H(1:8)', opts) ;
else
  warning('Refinement disabled as fminsearch was not found.') ;
end

% --------------------------------------------------------------------
%                                                         Show matches
% --------------------------------------------------------------------

dh1 = max(size(im2,1)-size(im1,1),0) ;
dh2 = max(size(im1,1)-size(im2,1),0) ;

figure(1) ; clf ;
subplot(2,1,1) ;
imagesc([padarray(im1,dh1,'post') padarray(im2,dh2,'post')]) ;
o = size(im1,2) ;
line([f1(1,matches(1,:));f2(1,matches(2,:))+o], ...
     [f1(2,matches(1,:));f2(2,matches(2,:))]) ;
title(sprintf('%d tentative matches', numMatches)) ;
axis image off ;

subplot(2,1,2) ;
imagesc([padarray(im1,dh1,'post') padarray(im2,dh2,'post')]) ;
o = size(im1,2) ;
line([f1(1,matches(1,ok));f2(1,matches(2,ok))+o], ...
     [f1(2,matches(1,ok));f2(2,matches(2,ok))]) ;
title(sprintf('%d (%.2f%%) inliner matches out of %d', ...
              sum(ok), ...
              100*sum(ok)/numMatches, ...
              numMatches)) ;
axis image off ;

drawnow ;
pause;

% --------------------------------------------------------------------
%                                                  epipolar line
% --------------------------------------------------------------------
% Finding Fundamental Matrix
%[FU FD FV]= svd (H);
%FDnew = FD;
%FDnew(3,3) = 0;
%FM = FU * FDnew * FV';
%FM

matchedPoints1 = X1(1:2,:)';
matchedPoints2 = X2(1:2,:)';
[FM, inliers] = estimateFundamentalMatrix(matchedPoints1,matchedPoints2,'Method', 'RANSAC', 'NumTrials', 2000, 'DistanceThreshold', 1e-4);
FM

subplot(2,1,1) ;
imshow(im1);
title('Inliers and Epipolar Lines in First Image'); hold on;
plot(matchedPoints1(inliers,1), matchedPoints1(inliers,2), 'go')
epiLines = epipolarLine(FM', matchedPoints2(inliers, :));
points = lineToBorderPoints(epiLines, size(im1));
line(points(:, [1,3])', points(:, [2,4])');
%line();

subplot(2,1,2) ;
imshow(im2);
title('Inliers and Epipolar Lines in Second Image'); hold on;
plot(matchedPoints2(inliers,1), matchedPoints2(inliers,2), 'go')
epiLines = epipolarLine(FM, matchedPoints1(inliers, :));
points = lineToBorderPoints(epiLines, size(im2));
line(points(:, [1,3])', points(:, [2,4])');

% calculate depth
% calculate disparity
disparity = matchedPoints1(inliers,1) - matchedPoints2(inliers,1);
dispmin = min(disparity)
dispmax = max(disparity)
dispavg = mean(disparity)
%[dispmin, dispmax] = [min(disparity), max(disparity)]
% Z = baseline * f / (d + doffs)
% get parameters from calib.txt
% image group 0
%baseline = 176.252;      % mm
%fLen = 4161.221;         % pixel
%doffs = 209.059;        % pixel     
% image group 1
baseline = 193.001;
fLen = 3979.911;
doffs = 124.343;
% image group 2
%baseline = 178.232;
%fLen = 2945.377;
%doffs = 170.681;
Z_max = baseline * fLen / (dispmin + doffs)
Z_min = baseline * fLen / (dispmax + doffs)
Z_avg = baseline * fLen / (dispavg + doffs)
end