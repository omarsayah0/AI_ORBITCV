#include "image.hpp"

cv::Mat	sobel_edge_image(const cv::Mat& image)
{
	cv::Mat	gray;
	cv::Mat	grad_x;
	cv::Mat	grad_y;
	cv::Mat	abs_x;
	cv::Mat	abs_y;
	cv::Mat	result;

	cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);

	cv::Sobel(gray, grad_x, CV_16S, 1, 0, 3);
	cv::Sobel(gray, grad_y, CV_16S, 0, 1, 3);

	cv::convertScaleAbs(grad_x, abs_x);
	cv::convertScaleAbs(grad_y, abs_y);

	cv::addWeighted(abs_x, 0.5, abs_y, 0.5, 0, result);

	cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
	return (result);
}