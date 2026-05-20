#include "image.hpp"

bool compute_homography(const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, cv::Mat& homography, cv::Mat& mask)
{
    std::vector<cv::Point2f> pts1;
    std::vector<cv::Point2f> pts2;

    for (size_t i = 0; i < good_matches.size(); i++)
    {
        pts1.push_back(kp1[good_matches[i].queryIdx].pt);
        pts2.push_back(kp2[good_matches[i].trainIdx].pt);
    }

    homography = cv::findHomography(pts2, pts1, cv::RANSAC, 3.0, mask);

    if (homography.empty())
    {
        std::cout << "Error: homography failed." << std::endl;
        return false;
    }

    return true;
}

void align_image(const cv::Mat& img2, const cv::Mat& homography,
     const cv::Size& output_size, cv::Mat& aligned)
{
    cv::warpPerspective(img2, aligned, homography, output_size);
}