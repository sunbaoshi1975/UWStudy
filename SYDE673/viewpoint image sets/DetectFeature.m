function [ features, fList, dList ] = DetectFeature(frame, rect, rNum)
%DetectFeature use SIFT to detect features and find descriptors
enlargeRect = [-50, -50, 100, 100];
[Fx, Fy, Fz] = size(frame);

h1=axes('Position',[0 0 1.0 1.0]);
h2=axes('Position',[rect(1)/Fy,rect(2)/Fx,rect(3)/Fy,rect(4)/Fx]);

hold off; axis normal; axis off;
axes(h1);
imshow(frame);   % draw image
rectangle('Position', [rect+enlargeRect], 'LineWidth',2, 'EdgeColor', 'b'); % draw tracker box
daspect([1,1,1])
axis off; axis image
%pause;

%axes('Position',[rect(1)/Fy,rect(2)/Fx,rect(3)/Fy,rect(4)/Fx]);
axes(h2);
subframe = frame(rect(2):rect(4)+rect(2)-1, rect(1):rect(3)+rect(1)-1,:);
[Lx, Ly, Lz] = size(subframe);
I = single(rgb2gray(subframe));

hold on;
%imshow(I);
%axis off; axis image

%image(I);
[f,d] = vl_sift(I);
features = size(f,2);

% Only keep features in the tracker box
%sel = f(1,:)>rect(1) & f(1,:)<rect(3) & f(2,:)>rect(2) & f(2,:)<rect(4);
sel = [1:features];
fA = f(:, sel); 
dA = d(:, sel);
features = size(fA,2);

% We visualize a random selection of 100 features
if rNum > 0
    perm = randperm(features);
    sel = perm(1:rNum);
else
    sel = [1:features];
end
fList = fA(:,sel);
dList = dA(:,sel);
h1 = vl_plotframe(fList);
h2 = vl_plotframe(fList);
set(h1,'color','k','linewidth',3);
set(h2,'color','y','linewidth',2);

% We can also overlay the descriptors
%h3 = vl_plotsiftdescriptor(d(:,sel),f(:,sel));
%set(h3,'color','g');
%features = 100;
%axes('Position', [1, 1, 1, 1]);
axis equal; axis off

end

