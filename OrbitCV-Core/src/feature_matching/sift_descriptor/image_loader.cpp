#include "image.hpp"

bool load_images(
    const std::string& path1,
    const std::string& path2,
    cv::Mat& img1,
    cv::Mat& img2
)
{
    img1 = cv::imread(path1);
    img2 = cv::imread(path2);

    if (img1.empty() || img2.empty())
    {
        std::cout << "Error: could not load images." << std::endl;
        return false;
    }
    return true;
}

void convert_to_gray(
    const cv::Mat& img,
    cv::Mat& gray
)
{
    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
}