import os
import cv2
import pydicom
import numpy as np

# Function to load DICOM image
def load_dicom_image(filepath):
    dicom_data = pydicom.dcmread(filepath)
    return dicom_data.pixel_array

# Function to count white dots in a black background
def count_white_dots(image, threshold_value=200):
    # Create a binary mask where white dots are detected
    _, binary_mask = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # Count the number of white pixels in the binary mask
    white_dot_count = np.sum(binary_mask == 255)  # Count pixels where the mask is white
    return white_dot_count

# Path to the DICOM image containing white dots
dicom_file_path = '3Dircadb1/3Dircadb1.1/MASKS_DICOM/artery/image_0'

# Load the DICOM image
image = load_dicom_image(dicom_file_path)

# Count the white dots in the image
num_white_dots = count_white_dots(image)

print(f"Number of white dots: {num_white_dots}")
