#include "image.hpp"

cv::Mat flip_image(const cv::Mat& image)
{
    cv::Mat result;

    cv::flip(image, result, 1);
    return (result);
}
