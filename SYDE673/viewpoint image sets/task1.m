%% Initialization
clear ; close all; clc

% run('C:/Program Files/MATLAB/vlfeat/toolbox/vl_setup')

trackbox = [800 320 640 480];
frame_matched = 0;
frame_removed = 0;
frame_inserted = 0;
fList = [0];
dList = [0];
randomNum = 100;

% Read video and track each frame
fileName = 'bird_clip.avi'; 
obj = VideoReader(fileName);
numFrames = obj.NumberOfFrames;    % The number of frame
fprintf('Total %d frames in the clip\n', numFrames);

for k = 1 : numFrames              % Read frames
    frame = read(obj,k);
    %imshow(frame);                % Display frame
    %imwrite(frame,strcat(num2str(k),'.jpg'),'jpg');    % Save frame

    % Track features' change between this frame and previous frame
    %nf = FeatureTracker(frame, k);
    if k == 1
        [frame_matched, fList, dList] = DetectFeature(frame, trackbox, randomNum);
        if randomNum > 0
            fprintf('%d features were randomly selected from %d features found the first frame...\n', randomNum, frame_matched);
        else
            fprintf('%d features found the the first frame...\n', frame_matched);
        end
        pause;
    else
        [nf, fList, dList] = MatchFeature(frame, trackbox, fList, dList, randomNum, k);
        fprintf('On frame %d matched %d feature(s), removed %d feature(s) and inserted %d feature(s)...\n', ...
            k, nf(1), nf(2), nf(3));
        if k < 5
            pause;
        end
    end
    
end