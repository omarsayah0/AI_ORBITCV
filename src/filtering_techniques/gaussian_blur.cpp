#include "image.hpp"

cv::Mat	gaussian_blur_image(const cv::Mat& image)
{
	cv::Mat	result;

	cv::GaussianBlur(image, result, cv::Size(5, 5), 0);
	return (result);
}
