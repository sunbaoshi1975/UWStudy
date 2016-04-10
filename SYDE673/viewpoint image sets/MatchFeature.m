function [ features, fList, dList ] = MatchFeature(frame, rect, fListA, dListA, rNum, imgIndex)
%MatchFeature use SIFT to detect features and find descriptors and macth
%with provided pair
enlargeRect = [-50, -50, 100, 100];
rectBig = rect+enlargeRect;
[Fx, Fy, Fz] = size(frame);

h1=axes('Position',[0 0 1.0 1.0]);
h2=axes('Position',[rectBig(1)/Fy,rectBig(2)/Fx,rectBig(3)/Fy,rectBig(4)/Fx]);

hold off; axis normal; axis off;
axes(h1);
if imgIndex < 5
    imshow(frame);   % draw image
    rectangle('Position', [rectBig+enlargeRect], 'LineWidth', 1, 'LineStyle', '-.', 'EdgeColor', 'b'); % draw even tracker box
end
daspect([1,1,1])
axis off; axis image
%pause;

% search features in a bigger region
[Fx, Fy, Fz] = size(frame);
subframe = frame(rectBig(2):rectBig(4)+rectBig(2)-1, rectBig(1):rectBig(3)+rectBig(1)-1,:);
[Lx, Ly, Lz] = size(subframe);
I = single(rgb2gray(subframe));
[fB,dB] = vl_sift(I);

% Macth
[matches, scores] = vl_ubcmatch(dListA, dB);
nMatch = size(matches, 2);
nRemoved = size(fListA, 2) - nMatch;
unMatched = setdiff(1:size(fB, 2), matches(2,:));
%size(unMatched)
fB1 = fB(:, unMatched);
%size(fB1)
dB1 = dB(:, unMatched);

% Find the center of matched list and calculate the new tracker box
%centerX = mean(fListA(1, matches(1,:))) + rect(1);
%centerY = mean(fListA(2, matches(1,:))) + rect(2);
%rectNew = [centerX - rect(3)/2, centerY - rect(4)/2, rect(3), rect(4)];
rectNew = rect;

% Only keep features in the tracker box
%rectBig(1)
%rectBig(2)
%rectNew
%fB(1,1:5)
%fB(2,1:5)
sel = logical(fB1(1,:)+rectBig(1)>rectNew(1) & fB1(1,:)+rectBig(1)<rectNew(1)+rectNew(3) & fB1(2,:)+rectBig(2)>rectNew(2) & fB1(2,:)+rectBig(2)<rectNew(2)+rectNew(4));
fB3 = fB1(:, sel);       % all in-box unmatched new features
dB3 = dB1(:, sel);
newFeatures = size(fB3, 2);
%size(fB, 2)
%size(fB2, 2)

% draw tracker box at new position
hold on;
if imgIndex < 5
    rectangle('Position', [rectNew + enlargeRect], 'LineWidth',2, 'EdgeColor', 'b'); % draw tracker box
end

% Update Lists
if rNum > 0
    perm = randperm(newFeatures);
    sel = perm(1:rNum);
else
    sel = [1:newFeatures];
end
fMatched = fListA(:, matches(1,:));
dMacthed = dListA(:, matches(1,:));
if newFeatures > 0
    fB4 = fB3(:,sel);
    dB4 = dB3(:,sel);
    nNew = size(fB4, 2);
    features = [nMatch nRemoved nNew];
    fList = [fMatched, fB4];
    dList = [dMacthed, dB4];
else
    fList = fMatched;
    dList = dMacthed;
    features = [nMatch nRemoved 0];
end

% draw features and especially mark out matched features
%axes('Position',[rectBig(1)/Fy,rectBig(2)/Fx,rectBig(3)/Fy,rectBig(4)/Fx]);
axes(h2);
if imgIndex < 5
    if newFeatures > 0
        h1 = vl_plotframe(fB4);
        h2 = vl_plotframe(fB4);
        set(h1,'color','k','linewidth',3);
        set(h2,'color','y','linewidth',2);
    end
    h1 = vl_plotframe(fMatched);
    h2 = vl_plotframe(fMatched);
    set(h1,'color','k','linewidth',3);
    set(h2,'color','r','linewidth',2);
end

% We can also overlay the descriptors
%h3 = vl_plotsiftdescriptor(d(:,sel),f(:,sel));
%set(h3,'color','g');
%features = 100;
%axes('Position', [1, 1, 1, 1]);
axis equal; axis off

end

