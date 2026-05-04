NAME = image
CXX = g++

SRC_DIR = src
OBJ_DIR = obj
INC_DIR = includes

SRCS = main.cpp crop.cpp flip.cpp print.cpp scale.cpp rotate.cpp affine.cpp perspective.cpp mouse.cpp draw.cpp
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
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all