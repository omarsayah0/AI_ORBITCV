#include "image.hpp"

cv::Mat	laplacian_edge_image(const cv::Mat& image)
{
	cv::Mat	gray;
	cv::Mat	blurred;
	cv::Mat	laplacian;
	cv::Mat	result;

	cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
	cv::GaussianBlur(gray, blurred, cv::Size(3, 3), 0);

	cv::Laplacian(blurred, laplacian, CV_16S, 3);
	cv::convertScaleAbs(laplacian, result);

	cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
	return (result);
}