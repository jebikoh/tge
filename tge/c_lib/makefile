CC=gcc

# Flags
PYTHON_CFLAGS := $(shell python3-config --cflags)
PYTHON_LDFLAGS := $(shell python3-config --ldflags)
CFLAGS=-Wall -Werror -fPIC $(PYTHON_CFLAGS)
LDFLAGS=$(PYTHON_LDFLAGS)


# INCLUDES
NUMPY_INCLUDE=$(shell python -c "import numpy; print(numpy.get_include())")


# Directories
SRC_DIR=src
INCLUDE_DIR=include
BUILD_DIR=build

# Target library
TARGET=$(BUILD_DIR)/tgelib.so

# Source and object files
SOURCES=$(wildcard $(SRC_DIR)/*.c)
OBJECTS=$(SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Default target
all: $(TARGET)

# Compile shared library
$(TARGET): $(OBJECTS)
	$(CC) -shared -o $@ $^ $(LDFLAGS)

# Compile object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -I$(NUMPY_INCLUDE) -c $< -o $@

# Clean up
clean:
	rm -f $(BUILD_DIR)/*.o $(TARGET)

.PHONY: all clean
