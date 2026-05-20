#include "image.hpp"

bool find_good_orb_matches(const cv::Mat& desc1,
    const cv::Mat& desc2, std::vector<cv::DMatch>& good_matches)
{
    cv::BFMatcher matcher(cv::NORM_HAMMING);
    std::vector<std::vector<cv::DMatch> > knn_matches;

    matcher.knnMatch(desc1, desc2, knn_matches, 2);

    for (size_t i = 0; i < knn_matches.size(); i++)
    {
        if (knn_matches[i].size() < 2)
            continue;
        if (knn_matches[i][0].distance < 0.75 * knn_matches[i][1].distance)
            good_matches.push_back(knn_matches[i][0]);
    }

    if (good_matches.size() < 4)
    {
        std::cout << "Error: not enough ORB good matches." << std::endl;
        return false;
    }
    return true;
}