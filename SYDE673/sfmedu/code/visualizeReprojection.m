function visualizeReprojection(graph, frames)
% SFMedu: Structrue From Motion for Education Purpose
% This function is added by Baoshi Sun as a part of assignment work
% Draw 3D keypoint point cloud proejected onto each images, as well as
% their observerd location.
figure
nCol = 3;
nRow = floor((frames.length - 1) / nCol + 1);

for frame=1:frames.length
    
    subplot(nRow, nCol, frame);
    image=imresize(imread(frames.images{frame}),frames.imsize(1:2));
    axis normal; axis off;
    
    % draw image
    imshow(image);
    
    % draw keypoints
    X = f2K(graph.f) * transformPtsByRt(graph.Str,graph.Mot(:,:,frame));
    xy = X(1:2,:) ./ X([3 3],:);    % 3D estimated location
    selector = find(graph.ObsIdx(frame,:)~=0);
    unselector = find(graph.ObsIdx(frame,:)==0);
    xyProjected = xy(:,selector);   % 3D estimated projected location on current image
    xyNoProjected = xy(:,unselector);   % 3D estimated projected location not on current image
    xyObs = graph.ObsVal(:,graph.ObsIdx(frame,selector));   % Observed location on current image
    oxyObs = zeros(2,size(selector,2));
    oxyObs(1,:)= size(image,2)/2 - xyObs(1,:);
    oxyObs(2,:)= size(image,1)/2 - xyObs(2,:);
    oxyProjected = zeros(2,size(selector,2));
    oxyProjected(1,:)= size(image,2)/2 - xyProjected(1,:);
    oxyProjected(2,:)= size(image,1)/2 - xyProjected(2,:);
    oxyNoProjected = zeros(2,size(unselector,2));
    oxyNoProjected(1,:)= size(image,2)/2 - xyNoProjected(1,:);
    oxyNoProjected(2,:)= size(image,1)/2 - xyNoProjected(2,:);
    hold on;
    plot(oxyObs(1,:), oxyObs(2,:), 'rx');
    plot(oxyProjected(1,:), oxyProjected(2,:), 'g+');
    plot(oxyNoProjected(1,:), oxyNoProjected(2,:), 'yo');
    for ln=1:size(selector)
        line([oxyObs(1,ln) oxyProjected(1,ln)], [oxyObs(2,ln) oxyProjected(2,ln)], 'Color', 'b', 'LineStyle', '-');
    end
end
