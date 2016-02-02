#CameraCalibration
--------------------------------------------------------------------
Camera Calibration code for Chessboard pattern at Srujana: Center for Innovation, LV Prasad Eye Institute, Hyderabad.

Author: Tejaswi Kasarla (Intern at Srujana)

-------------------------------------------------------------------

This code was taken directly from the OpenCV tutorials and edited to suit our needs. All due credits to the original author. 

Open CV needs to be installed before compiling the program

-------------------------------------------------------------------

Download the sourcefile and the xml file to the same directory and go to that directoy in terminal

This program can be complied by typing the following code in terminal (Ubuntu 15.04)

		g++ -Iusr/include/opencv2 camera_calibration.cpp $(pkg-config opencv --libs)

the a.out file generated after the compilation can be run from the terminal. 

--------------------------------------------------------------------

Important: In the xml file use the <Input>"1"</Input> only if you have an external USB wecam connected to your laptop
		   
	If it's the default camera you want to calibrate change the 1 to 0
		   
--------------------------------------------------------------------

This program once run opens a live feed of the camera. Hold the chessboard pattern against the webcam. 15 snapshots of the chessboard pattern are taken after which camera is calibrated and a out_camera_data.xml file is generated in the same directory of your program. A sample output file had been uploaded. 

--------------------------------------------------------------------

Note: Although originally intended for camera calibration at Srujana, any others can calibrate the camera by downloading the A4_Chess.png file and printing it out on an A4 sheet. Measure the side of the square and change it accordingly in the xml file in millimeters. Guys at Srujana can directly download and complie the code without any changes.

-------------------------------------------------------------------

For detailed explanation of the code visit the OpenCV documentation here : http://docs.opencv.org/doc/tutorials/calib3d/camera_calibration/camera_calibration.html#the-calibration-and-save
