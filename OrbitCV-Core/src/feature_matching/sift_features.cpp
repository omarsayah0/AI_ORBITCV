#include "image.hpp"

bool compute_sift_features(const cv::Mat& gray,
     std::vector<cv::KeyPoint>& keypoints, cv::Mat& descriptors)
{
    cv::Ptr<cv::SIFT> sift;

    sift = cv::SIFT::create();
    sift->detectAndCompute(gray, cv::noArray(), keypoints, descriptors);

    if (descriptors.empty())
    {
        std::cout << "Error: no descriptors found." << std::endl;
        return false;
    }
    return true;
}