NAME = image
CXX = g++

SRC_DIR = src
OBJ_DIR = obj
INC_DIR = includes
GT = geometric_transformations
FT = filtering_techniques
FM = feature_matching
S = sift_descriptor
O = orb_descriptor

SRCS =	main.cpp \
		$(GT)/crop.cpp \
		$(GT)/flip.cpp \
		print.cpp \
		$(GT)/scale.cpp \
		$(GT)/rotate.cpp \
		$(GT)/affine.cpp \
		$(GT)/perspective.cpp \
		$(GT)/mouse.cpp \
		draw.cpp \
		$(FT)/bilateral_filter.cpp \
		$(FT)/gaussian_blur.cpp \
		$(FT)/laplacian_edge.cpp \
		$(FT)/median_blur.cpp \
		$(FT)/sharpening_filter.cpp \
		$(FT)/sobel_edge.cpp \
		$(FM)/$(S)/sift_features.cpp \
		$(FM)/$(S)/image_loader.cpp \
		$(FM)/$(S)/matcher.cpp \
		$(FM)/$(S)/homography.cpp \
		$(FM)/$(S)/display.cpp \
		$(FM)/$(S)/sift_align_images.cpp \
		$(FM)/$(O)/orb_features.cpp \
		$(FM)/$(O)/image_loader.cpp \
		$(FM)/$(O)/matcher.cpp \
		$(FM)/$(O)/homography.cpp \
		$(FM)/$(O)/display.cpp \
		$(FM)/$(O)/orb_align_images.cpp


OBJS = $(SRCS:%.cpp=$(OBJ_DIR)/%.o)

CXXFLAGS = -I$(INC_DIR) $(shell pkg-config --cflags opencv4)
OPENCV_LIBS = $(shell pkg-config --libs opencv4)

all: $(NAME)

setup:
	sudo apt update
	sudo apt install g++ pkg-config libopencv-dev

$(NAME): $(OBJS)
	$(CXX) $(OBJS) -o $(NAME) $(OPENCV_LIBS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all