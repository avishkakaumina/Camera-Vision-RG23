import cv2
import numpy as np
from PIL import Image

# Function to detect the color
def detect_color(frame):
    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #print(hsv)
    
    # Define the lower and upper boundaries of the color you want to detect (in HSV)
    lower_bound = np.array([100, 100, 100])  # Lower bound of the color (here, it's for green color)
    upper_bound = np.array([140, 255, 255])  # Upper bound of the color (here, it's for green color)
    
    # Create a mask for the specified color range
    global mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    return res

# Open a video capture object (you can replace '0' with your video file name if you want to process a video)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    
    # Call the detect_color function to get the detected color in the frame
    detected_color = detect_color(frame)

    # Apply Canny edge detection (example)
    edges = cv2.Canny(mask, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.4 * cv2.arcLength(contour, True)
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
        cv2.putText(frame, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    


    mask_box_b = Image.fromarray(mask)
    bbox_b = mask_box_b.getbbox()
    if bbox_b is not None:
        x1, y1, x2, y2 = bbox_b
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 265, 0), 2)


    
    # Display the original frame and the detected color
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Detected Color', detected_color)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
