#include "image.hpp"

void display_orb_results(const cv::Mat& img1, const cv::Mat& img2,
    const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, const cv::Mat& aligned)
{
    cv::Mat matches_img;
    cv::drawMatches(img1, kp1, img2, kp2, good_matches, matches_img);

    cv::imshow("ORB Feature Matches", matches_img);
    cv::imshow("ORB Aligned Image", aligned);
    cv::waitKey(0);
    cv::destroyWindow("ORB Feature Matches");
    cv::destroyWindow("ORB Aligned Image");
}