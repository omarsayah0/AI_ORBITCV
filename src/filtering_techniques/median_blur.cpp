#include "image.hpp"

cv::Mat	median_filter_image(const cv::Mat& image)
{
	cv::Mat	result;

	cv::medianBlur(image, result, 5);
	return (result);
}