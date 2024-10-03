import pydicom
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to load DICOM image
def load_dicom_image(filepath):
    dicom_data = pydicom.dcmread(filepath)
    image = dicom_data.pixel_array
    return image

# Function to apply windowing
def apply_windowing(image, window_center, window_width):
    window_min = window_center - (window_width / 2)
    window_max = window_center + (window_width / 2)
    image = np.clip(image, window_min, window_max)
    return ((image - window_min) / (window_max - window_min) * 255).astype(np.uint8)

# Organ window settings
organ_window_settings = {
    'Liver': (50, 100),
    'Kidney': (40, 100),
    'Bone': (300, 1500),
}

# Function to apply windowing based on organ
def apply_window_for_organ(dicom_image, organ):
    if organ in organ_window_settings:
        window_center, window_width = organ_window_settings[organ]
    else:
        raise ValueError(f"Unknown organ '{organ}'. Available options are: {list(organ_window_settings.keys())}")
    
    return apply_windowing(dicom_image.pixel_array, window_center, window_width)

# Function to extract white dots using thresholding
def extract_white_dots(image, threshold_value=200):
    _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, kernel)
    return cleaned_image

# Function to overlay white dots onto the windowed patient image in blue
def overlay_white_dots_on_image(base_image, dots_image):
    base_image_rgb = cv2.cvtColor(base_image, cv2.COLOR_GRAY2RGB)
    r, g, b = cv2.split(base_image_rgb)
    b[dots_image == 255] = 255  # Set blue channel to 255 where the dots are
    r[dots_image == 255] = 0    # Set red channel to 0 to prevent yellow
    g[dots_image == 255] = 0    # Set green channel to 0 to prevent yellow
    overlay_image = cv2.merge([r, g, b])
    return overlay_image

# Load the original patient DICOM image
original_dicom_path = '3Dircadb1/3Dircadb1.1/PATIENT_DICOM/image_0'
original_image = pydicom.dcmread(original_dicom_path)

# Apply windowing to the patient image based on organ (e.g., Liver)
windowed_patient_image = apply_window_for_organ(original_image, 'Liver')

# Load the DICOM image containing the white dots
dots_dicom_path = '3Dircadb1/3Dircadb1.1/MASKS_DICOM/artery/image_0'
dots_image = load_dicom_image(dots_dicom_path)

# Extract white dots from the dots image
white_dots = extract_white_dots(dots_image, threshold_value=200)

# Overlay the white dots onto the windowed patient image with blue color
overlay_image = overlay_white_dots_on_image(windowed_patient_image, white_dots)

# Plot and display the windowed patient image and the overlayed image
plt.figure(figsize=(12, 6))

# Display the windowed patient image
plt.subplot(1, 2, 1)
plt.imshow(windowed_patient_image, cmap='gray')
plt.title('Windowed Patient Image')
plt.axis('off')

# Display the windowed patient image with blue dots overlay
plt.subplot(1, 2, 2)
plt.imshow(overlay_image)
plt.title('Windowed Patient Image with Blue Dots Overlay')
plt.axis('off')

plt.show()
