#include "image.hpp"

cv::Mat rotate_image(const cv::Mat& image)
{
    cv::Mat result;
    
    cv::Point2f center(image.cols / 2.0f, image.rows /2.0f);

    cv::Mat matrix = cv::getRotationMatrix2D(center, 30, 1.0);

    cv::warpAffine(image, result, matrix, image.size());
    
    return (result);
}