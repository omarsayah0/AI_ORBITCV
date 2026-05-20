#include "image.hpp"

int  main()
{
    cv::Mat pre_image = cv::imread("input/image.jpeg");

    if (pre_image.empty())
    {
        std::cout << "Error: Could not load the image!\n";
        return (1);
    }

    cv::Mat image;
    cv::resize(pre_image, image, cv::Size(1200, 800)); 

    cv::Mat current_image = image.clone();

    print_menu();
    
    while (true)
    {
        cv::Mat display = current_image.clone();

        draw_menu(display);
        cv::imshow("Smart Image Transform Playground", display);

        char key = static_cast<char>(cv::waitKey(0));
        
        if (key == 'q' || key == 27)
            break;
        else if (key == 'o')
            current_image = image.clone();
        else if (key == 'c')
            current_image = crop_image(current_image);
        else if (key == 'm')
	        current_image = mouse_crop_image(current_image);
        else if (key == 'f')
            current_image = flip_image(current_image);
        else if (key == 's')
            current_image = scale_image(current_image);
        else if (key == 'r')
            current_image = rotate_image(current_image);
        else if (key == 'a')
            current_image = affine_image(current_image);
        else if (key == 'p')
            current_image = perspective_image(current_image);
        else if (key == 'g')
	        current_image = gaussian_blur_image(current_image);
        else if (key == 'n')
	        current_image = median_filter_image(current_image);
        else if (key == 'b')
	        current_image = bilateral_filter_image(current_image);
        else if (key == 'h')
        	current_image = sharpen_image(current_image);
        else if (key == 'e')
        	current_image = sobel_edge_image(current_image);
        else if (key == 'l')
        	current_image = laplacian_edge_image(current_image);
        else if (key == 'x')
            sift_align_images();
        else if (key == 'z')
            orb_align_images();
    }

    cv::destroyAllWindows();
    return (0);
}