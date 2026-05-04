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

#endif