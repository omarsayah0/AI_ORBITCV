#include "image.hpp"

void sift_align_images()
{
    cv::Mat img1;
    cv::Mat img2;
    cv::Mat gray1;
    cv::Mat gray2;
    cv::Mat desc1;
    cv::Mat desc2;
    cv::Mat homography;
    cv::Mat aligned;
    std::vector<cv::KeyPoint> kp1;
    std::vector<cv::KeyPoint> kp2;
    std::vector<cv::DMatch> good_matches;

    if (!load_images("input/image.jpeg", "input/second.jpg", img1, img2))
        return;

    convert_to_gray(img1, gray1);
    convert_to_gray(img2, gray2);

    if (!compute_sift_features(gray1, kp1, desc1))
        return;
    if (!compute_sift_features(gray2, kp2, desc2))
        return;

    if (!find_good_matches(desc1, desc2, good_matches))
        return;

    if (!compute_homography(kp1, kp2, good_matches, homography))
        return;

    align_image(img2, homography, img1.size(), aligned);

    show_results(img1, img2, kp1, kp2, good_matches, aligned);
}