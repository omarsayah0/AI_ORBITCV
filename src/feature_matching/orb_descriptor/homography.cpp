#include "image.hpp"

bool compute_orb_homography(const cv::Mat& img1, const cv::Mat& img2,
    std::vector<cv::KeyPoint>& kp1, std::vector<cv::KeyPoint>& kp2,
    std::vector<cv::DMatch>& good_matches, cv::Mat& homography, cv::Mat& mask)
{
    cv::Mat gray1;
    cv::Mat gray2;
    cv::Mat desc1;
    cv::Mat desc2;

    cv::cvtColor(img1, gray1, cv::COLOR_BGR2GRAY);
    cv::cvtColor(img2, gray2, cv::COLOR_BGR2GRAY);

    if (!compute_orb_features(gray1, kp1, desc1) ||
        !compute_orb_features(gray2, kp2, desc2))
    {
        return false;
    }

    if (!find_good_orb_matches(desc1, desc2, good_matches))
        return false;

    std::vector<cv::Point2f> pts1;
    std::vector<cv::Point2f> pts2;

    for (const auto& match : good_matches)
    {
        pts1.push_back(kp1[match.queryIdx].pt);
        pts2.push_back(kp2[match.trainIdx].pt);
    }

    homography = cv::findHomography(pts2, pts1, cv::RANSAC, 3.0, mask);

    if (homography.empty())
    {
        std::cout << "Error: ORB homography failed." << std::endl;
        return false;
    }

    return true;
}