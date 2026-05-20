#include "image.hpp"

bool load_images_orb(cv::Mat& img1, cv::Mat& img2)
{
    img1 = cv::imread("input/image.jpeg");
    img2 = cv::imread("input/second.jpg");

    if (img1.empty() || img2.empty())
    {
        std::cout << "Error: could not load input images." << std::endl;
        return false;
    }

    return true;
}