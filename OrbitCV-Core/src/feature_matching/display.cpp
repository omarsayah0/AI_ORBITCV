#include "image.hpp"

void show_results(const cv::Mat& img1, const cv::Mat& img2,
    const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, const cv::Mat& aligned)
{
    cv::Mat match_img;

    cv::drawMatches(
        img1,
        kp1,
        img2,
        kp2,
        good_matches,
        match_img
    );

    cv::imshow("SIFT Feature Matches", match_img);
    cv::imshow("Reference Image", img1);
    cv::imshow("Aligned Second Image", aligned);
    cv::waitKey(0);
}