import cv2
import numpy as np

# Function to detect the color
def detect_color(frame):
    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper boundaries of the color you want to detect (in HSV)
    lower_bound = np.array([30, 50, 50])  # Lower bound of the color (here, it's for green color)
    upper_bound = np.array([90, 255, 255])  # Upper bound of the color (here, it's for green color)
    
    # Create a mask for the specified color range
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
    
    # Display the original frame and the detected color
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Detected Color', detected_color)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()