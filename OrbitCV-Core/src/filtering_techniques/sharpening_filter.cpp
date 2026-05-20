#include "image.hpp"

cv::Mat	sharpen_image(const cv::Mat& image)
{
	cv::Mat	result;
	cv::Mat	kernel;

	kernel = (cv::Mat_<float>(3, 3) <<
		0, -1, 0,
		-1, 5, -1,
		0, -1, 0);

	cv::filter2D(image, result, image.depth(), kernel);
	return (result);
}