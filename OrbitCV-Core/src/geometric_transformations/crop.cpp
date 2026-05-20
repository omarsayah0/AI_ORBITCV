#include "image.hpp"


cv::Mat crop_image(const cv::Mat & image)
{
    int x = image.cols / 4;
    int y = image.rows / 4;
    int w = image.cols / 2;
    int h = image.rows / 2;

    cv::Rect croped_area(x, y, w, h);
    return (image(croped_area).clone());
}