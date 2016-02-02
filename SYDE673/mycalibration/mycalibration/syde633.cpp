#include <opencv\cv.h>
#include <opencv\highgui.h>

int main(int argc, char** argv[])
{
	IplImage* src = cvLoadImage("../IMG_4255.JPG", CV_LOAD_IMAGE_GRAYSCALE);
	cvNamedWindow("Src", CV_WINDOW_AUTOSIZE);
	cvShowImage("Src", src);
	cvWaitKey(0);
	cvReleaseImage(&src);
	cvDestroyAllWindows();

	return 0;
}