#include "image.hpp"


cv::Mat scale_image(const cv::Mat& image)
{
    cv::Mat result;

    cv::resize(image, result, cv::Size(400, 400), 0, 0, cv::INTER_LINEAR);

    return (result);
}