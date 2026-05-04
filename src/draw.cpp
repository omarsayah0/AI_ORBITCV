#include "image.hpp"

void draw_menu(cv::Mat& img)
{
    int y = 30;

    cv::putText(img, "Controls:",
        cv::Point(20, y),
        cv::FONT_HERSHEY_SIMPLEX, 0.7,
        cv::Scalar(255,255,255), 2);

    y += 30;

    cv::putText(img, "o: original", cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "c: crop",     cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "m: mouse crop",cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "f: flip",     cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "s: scale",    cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "r: rotate",   cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "a: affine",   cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "p: perspective",cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1); y+=25;
    cv::putText(img, "q: quit",     cv::Point(20,y), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0,255,0),1);
}