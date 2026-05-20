#include "image.hpp"

static cv::Mat g_image;
static cv::Mat g_display;
static cv::Point g_start;
static cv::Point g_end;
static bool g_drawing = false;
static bool g_selected = false;

static void draw_ui(cv::Mat& img)
{
    cv::putText(img, "Drag mouse to select ROI",
                cv::Point(20, 30),
                cv::FONT_HERSHEY_SIMPLEX, 0.6,
                cv::Scalar(0, 255, 0), 1);

    cv::putText(img, "c: confirm  r: reset  q/ESC: cancel",
                cv::Point(20, 60),
                cv::FONT_HERSHEY_SIMPLEX, 0.6,
                cv::Scalar(0, 255, 0), 1);
}

static void mouse_callback(int event, int x, int y, int, void *)
{
    if (event == cv::EVENT_LBUTTONDOWN)
    {
        g_drawing = true;
        g_selected = false;
        g_start = cv::Point(x, y);
        g_end = g_start; 
    }
    else if (event == cv::EVENT_MOUSEMOVE && g_drawing)
    {
        g_end = cv::Point(x, y);
        g_display = g_image.clone();
        draw_ui(g_display);
        cv::rectangle(g_display, g_start, g_end, cv::Scalar(0, 255, 0), 2);
    }
    else if (event == cv::EVENT_LBUTTONUP)
    {
        g_drawing = false;
        g_selected = true;
        g_end = cv::Point(x, y);
        g_display = g_image.clone();
        draw_ui(g_display);
        cv::rectangle(g_display, g_start, g_end, cv::Scalar(0, 255, 0), 2);
    }
}

cv::Rect get_valid_rec(void)
{
    int x = std::min(g_start.x, g_end.x);
    int y = std::min(g_start.y, g_end.y);
    int w = std::abs(g_end.x - g_start.x);
    int h = std::abs(g_end.y - g_start.y);

    cv::Rect roi(x, y, w, h);

    return(roi);
}

cv::Mat mouse_crop_image(const cv::Mat& image)
{
    cv::Rect roi;

    g_image = image.clone();
    g_display = g_image.clone();
    draw_ui(g_display);
    g_selected = false;

    cv::namedWindow("Selected ROI");
    cv::setMouseCallback("Selected ROI", mouse_callback);

    while (true)
    {
        cv::imshow("Selected ROI", g_display);
        
        char key = static_cast<char>(cv::waitKey(20));

        if (key == 'q' || key == 27)
            break;
        if (key == 'r')
        {
            g_selected = false;
            g_display = g_image.clone();
            draw_ui(g_display);
        }
        if (key == 'c' && g_selected)
        {
            roi = get_valid_rec();
            if (roi.width > 0 && roi.height > 0)
			{
				cv::destroyWindow("Selected ROI");
				return (g_image(roi).clone());
			}
        }
    }
    cv::destroyWindow("Selected ROI");
	return (image.clone());
}