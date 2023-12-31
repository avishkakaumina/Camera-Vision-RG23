import cv2
import numpy as np

# Read the image
image = cv2.imread('pic1.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection (example)
edges = cv2.Canny(gray, 50, 150)

# Thresholding to segment the object (adjust threshold value as needed)
_, binary_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Create an all-green image with the same size as the original image
green_mask = np.zeros_like(image)
green_mask[:] = [0, 255, 0]  # Green color in BGR format

# Apply the binary mask to the green mask to selectively change object color to green
green_object = cv2.bitwise_and(green_mask, green_mask, mask=binary_mask)

#Use cv2.findContours() to find the contours of the shapes in the binary image.
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Get the number of vertices (shape detection logic)
    num_vertices = len(approx)

    if num_vertices == 3:
        shape_name = "Triangle"
    elif num_vertices == 4:
        shape_name = "Rectangle or Square"
    elif num_vertices == 5:
        shape_name = "Pentagon"
    else:
        shape_name = "Circle"

    # Draw the shape name on the image
    x, y = approx.ravel()[0], approx.ravel()[1] - 10
    cv2.putText(green_object, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
# Display the result
cv2.imshow('Original Image', image)
cv2.imshow('Shapes Detected', green_object)
cv2.waitKey(0)
cv2.destroyAllWindows()
 

