#include "image.hpp"

bool orb_align_images(void)
{
    cv::Mat img1;
    cv::Mat img2;
    cv::Mat homography;
    cv::Mat mask;
    cv::Mat aligned;

    std::vector<cv::KeyPoint> kp1;
    std::vector<cv::KeyPoint> kp2;
    std::vector<cv::DMatch> good_matches;

    auto start = std::chrono::high_resolution_clock::now();

    if (!load_images_orb(img1, img2))
        return false;

    if (!compute_orb_homography(
            img1,
            img2,
            kp1,
            kp2,
            good_matches,
            homography,
            mask))
    {
        return false;
    }

    cv::warpPerspective(img2, aligned, homography, img1.size());

    auto end = std::chrono::high_resolution_clock::now();
    double time_ms =
        std::chrono::duration<double, std::milli>(end - start).count();

    int inliers = cv::countNonZero(mask);

    std::cout << "\n=== ORB Results ===" << std::endl;
    std::cout << "Image 1 keypoints: " << kp1.size() << std::endl;
    std::cout << "Image 2 keypoints: " << kp2.size() << std::endl;
    std::cout << "Good matches: " << good_matches.size() << std::endl;
    std::cout << "RANSAC inliers: " << inliers << std::endl;
    std::cout << "Runtime: " << time_ms << " ms" << std::endl;

    display_orb_results(img1, img2, kp1, kp2, good_matches, aligned);

    return true;
}