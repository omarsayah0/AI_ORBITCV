#include "image.hpp"


cv::Mat perspective_image(const cv::Mat& image)
{
    cv::Mat result;

    cv::Point2f src[4];
    cv::Point2f dest[4];

    int w = image.cols;
    int h = image.rows;

    src[0] = cv::Point2f(w * 0.25f, h * 0.25f);
    src[1] = cv::Point2f(w * 0.75f, h * 0.20f);
    src[2] = cv::Point2f(w * 0.20f, h * 0.75f);
    src[3] = cv::Point2f(w * 0.80f, h * 0.80f);

    //To see the point of view of the perspective
    // cv::Mat presp = image.clone();
    // cv::circle(presp, src[0], 8, cv::Scalar(0, 0, 255), -1);
    // cv::circle(presp, src[1], 8, cv::Scalar(0, 255, 0), -1);
    // cv::circle(presp, src[2], 8, cv::Scalar(255, 0, 0), -1);
    // cv::circle(presp, src[3], 8, cv::Scalar(0, 255, 255), -1);
    // cv::line(presp, src[0], src[1], cv::Scalar(255,255,255), 2);
    // cv::line(presp, src[1], src[3], cv::Scalar(255,255,255), 2);
    // cv::line(presp, src[3], src[2], cv::Scalar(255,255,255), 2);
    // cv::line(presp, src[2], src[0], cv::Scalar(255,255,255), 2);
    // cv::imshow("SRC Points", presp);
    // cv::waitKey(0);


    dest[0] = cv::Point2f(0, 0);
    dest[1] = cv::Point2f(400 ,0);
    dest[2] = cv::Point2f(0, 400);
    dest[3] = cv::Point2f(400, 400);

    cv::Mat matrix = cv::getPerspectiveTransform(src, dest);

    cv::warpPerspective(image, result, matrix, image.size());

    return (result);
}