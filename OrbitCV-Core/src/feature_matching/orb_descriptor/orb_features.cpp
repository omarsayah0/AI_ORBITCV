#include "image.hpp"


bool compute_orb_features(const cv::Mat& gray,
    std::vector<cv::KeyPoint>& keypoints, cv::Mat& descriptors)
{
    cv::Ptr<cv::ORB> orb = cv::ORB::create(2000);
    orb->detectAndCompute(gray, cv::noArray(), keypoints, descriptors);

    if (keypoints.empty() || descriptors.empty())
    {
        std::cout << "Error: ORB could not find features." << std::endl;
        return false;
    }
    return true;
}