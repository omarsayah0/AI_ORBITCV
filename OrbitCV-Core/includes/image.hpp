#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <opencv2/opencv.hpp>
#include <iostream>

cv::Mat crop_image(const cv::Mat & image);
cv::Mat flip_image(const cv::Mat& image);
void    print_menu();
cv::Mat scale_image(const cv::Mat& image);
cv::Mat rotate_image(const cv::Mat& image);
cv::Mat affine_image(const cv::Mat& image);
cv::Mat perspective_image(const cv::Mat& image);
cv::Mat mouse_crop_image(const cv::Mat& image);
void    draw_menu(cv::Mat& img);
cv::Mat	gaussian_blur_image(const cv::Mat& image);
cv::Mat	median_filter_image(const cv::Mat& image);
cv::Mat	bilateral_filter_image(const cv::Mat& image);
cv::Mat	sharpen_image(const cv::Mat& image);
cv::Mat	sobel_edge_image(const cv::Mat& image);
cv::Mat	laplacian_edge_image(const cv::Mat& image);

//sift
bool load_images( const std::string& path1,
     const std::string& path2, cv::Mat& img1, cv::Mat& img2);

void convert_to_gray( const cv::Mat& img, cv::Mat& gray);

bool compute_sift_features(const cv::Mat& gray,
    std::vector<cv::KeyPoint>& keypoints, cv::Mat& descriptors);

bool find_good_matches(const cv::Mat& desc1, const cv::Mat& desc2,
     std::vector<cv::DMatch>& good_matches);

bool compute_homography(const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, cv::Mat& homography, cv::Mat& mask);

void align_image(const cv::Mat& img2, const cv::Mat& homography,
     const cv::Size& output_size, cv::Mat& aligned);

void show_results(const cv::Mat& img1, const cv::Mat& img2,
    const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, const cv::Mat& aligned);

void sift_align_images();



//orb
bool compute_orb_features(const cv::Mat& gray,
    std::vector<cv::KeyPoint>& keypoints, cv::Mat& descriptors);

bool find_good_orb_matches(const cv::Mat& desc1,
    const cv::Mat& desc2, std::vector<cv::DMatch>& good_matches);

void display_orb_results(const cv::Mat& img1, const cv::Mat& img2,
    const std::vector<cv::KeyPoint>& kp1, const std::vector<cv::KeyPoint>& kp2,
    const std::vector<cv::DMatch>& good_matches, const cv::Mat& aligned);

bool load_images_orb(cv::Mat& img1, cv::Mat& img2);

bool orb_align_images(void);

bool compute_orb_homography(const cv::Mat& img1, const cv::Mat& img2,
    std::vector<cv::KeyPoint>& kp1, std::vector<cv::KeyPoint>& kp2,
    std::vector<cv::DMatch>& good_matches, cv::Mat& homography, cv::Mat& mask);

#endif