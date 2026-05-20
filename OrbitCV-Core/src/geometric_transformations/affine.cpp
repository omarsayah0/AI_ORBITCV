#include "image.hpp"

cv::Mat affine_image(const cv::Mat& image)
{
    cv::Mat result;

    cv::Point2f src[3];
    cv::Point2f dest[3];

    src[0] = cv::Point2f(50, 50);
    src[1] = cv::Point2f(200, 50);
    src[2] = cv::Point2f(50, 200);

    dest[0] = cv::Point2f(20, 100);
    dest[1] = cv::Point2f(220, 50);
    dest[2] = cv::Point2f(100, 250);

    cv::Mat matrix = cv::getAffineTransform(src, dest);

    cv::warpAffine(image, result, matrix, image.size());

    return (result);
}