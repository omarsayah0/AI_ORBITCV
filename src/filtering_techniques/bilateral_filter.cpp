#include "image.hpp"

cv::Mat	bilateral_filter_image(const cv::Mat& image)
{
	cv::Mat	result;

	cv::bilateralFilter(image, result, 9, 75, 75);
	return (result);
}