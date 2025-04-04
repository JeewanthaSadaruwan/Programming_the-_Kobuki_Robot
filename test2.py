#detect the colors in middle cell while rotatin





import cv2
import numpy as np
import threading
import time as t

# Color ranges in HSV
LOWER_RED1 = np.array([0, 100, 100])
UPPER_RED1 = np.array([10, 255, 255])
LOWER_RED2 = np.array([160, 100, 100])
UPPER_RED2 = np.array([180, 255, 255])

LOWER_BLUE = np.array([100, 100, 100])
UPPER_BLUE = np.array([130, 255, 255])

LOWER_GREEN = np.array([40, 100, 100])
UPPER_GREEN = np.array([80, 255, 255])

LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([35, 255, 255])

# Minimum contour area to filter out noise
MIN_CONTOUR_AREA = 500

def rotate_robot(kobuki, duration, stop_event):
    """
    Rotate the robot for a specified duration or until a target color is detected
    
    Args:
        kobuki: Robot control object
        duration (float): Maximum rotation duration in seconds
        stop_event (threading.Event): Event to signal when to stop rotation
    """
    start_time = t.time()
    while t.time() - start_time < duration and not stop_event.is_set():
        kobuki.move(-160, 80, 1)  # Left rotation
        t.sleep(0.1)
    
    # Stop the robot after duration or when stopped by detection
    kobuki.move(0, 0, 1)

def detect_color_boxes(frame, target_colors, detected_colors, detected_target, stop_event):
    """
    Detect color boxes in the center third of the frame,
    stop if any target color is detected in the center region
    
    Args:
        frame (numpy.ndarray): Input frame to process
        target_colors (list): List of colors to look for
        detected_colors (dict): Dictionary to store detected color information
        detected_target (list): List to store the first detected target color
        stop_event (threading.Event): Event to signal when to stop rotation
    
    Returns:
        numpy.ndarray: Processed frame with color box detections
        bool: True if any target color was detected in the center region
    """
    # Get frame dimensions
    height, width = frame.shape[:2]
    
    # Define the center third of the frame
    left_boundary = width // 3
    right_boundary = 2 * width // 3
    
    # Draw vertical lines to show the frame division
    cv2.line(frame, (left_boundary, 0), (left_boundary, height), (255, 255, 255), 1)
    cv2.line(frame, (right_boundary, 0), (right_boundary, height), (255, 255, 255), 1)
    
    # Add text labels for each region
    cv2.putText(frame, "Left", (width//6, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "Center", (width//2, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "Right", (5*width//6, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create masks for each color
    # Red mask combines two ranges
    red_mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    red_mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    
    blue_mask = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
    green_mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
    yellow_mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
    
    # Apply morphological operations to clean up the masks
    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours for each color
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Color detection colors
    color_map = {
        'red': (0, 0, 255),      # BGR for Red
        'blue': (255, 0, 0),     # BGR for Blue
        'green': (0, 255, 0),    # BGR for Green
        'yellow': (0, 255, 255)  # BGR for Yellow
    }
    
    # Process and draw bounding boxes for each color
    colors_contours = [
        ('red', red_contours),
        ('blue', blue_contours),
        ('green', green_contours),
        ('yellow', yellow_contours)
    ]
    
    target_detected = False
    center_detections = {
        'red': False,
        'blue': False,
        'green': False,
        'yellow': False
    }
    
    for color_name, contours in colors_contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_CONTOUR_AREA:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate center point of the bounding box
                center_x = x + w // 2
                
                # Determine the region of the bounding box center
                region = "left" if center_x < left_boundary else "right" if center_x >= right_boundary else "center"
                
                # Store detected color information
                detected_colors[color_name].append({
                    'contour': contour,
                    'area': area,
                    'region': region
                })
                
                # Draw rectangle with different styles based on region
                if region == "center":
                    # Highlight boxes in the center region with thicker lines
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_map[color_name], 3)
                    center_detections[color_name] = True
                else:
                    # Normal style for other regions
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color_map[color_name], 1)
                
                # Put text with region info
                cv2.putText(frame, f"{color_name.capitalize()} ({region})", 
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[color_name], 2)
                
                # Print detection info
                print(f"{color_name.capitalize()} box detected in {region} region at ({x}, {y}), size: {w}x{h}")
                
                # Check if this is a target color in the center region
                if color_name in target_colors and region == "center" and not target_detected:
                    detected_target[0] = color_name
                    target_detected = True
                    print(f"Target color {color_name} detected in center region! Stopping rotation.")
                    stop_event.set()
    
    # Add color detection status on the frame
    height = frame.shape[0]
    offset = 30
    
    # Display detection status for each color
    color_names = ['red', 'blue', 'green', 'yellow']
    for i, color in enumerate(color_names):
        status_text = f"{color.capitalize()}: "
        
        if center_detections[color]:
            status_text += "CENTER"
            color_status = color_map[color]
        elif any(d['color_name'] == color for d in detected_colors[color]):
            status_text += "Detected (not in center)"
            color_status = (200, 200, 200)
        else:
            status_text += "Not Detected"
            color_status = (200, 200, 200)
        
        # Highlight target colors
        if color in target_colors:
            status_text += " (Target)"
        
        cv2.putText(frame, status_text, (10, height - (len(color_names) - i)*offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_status, 2)
    
    return frame, target_detected

def detect_colors(duration, target_colors, detected_colors, detected_target, stop_event):
    """
    Perform color detection continuously, looking for target colors in center region
    
    Args:
        duration (float): Maximum detection duration in seconds
        target_colors (list): List of colors to look for
        detected_colors (dict): Dictionary to store detected color information
        detected_target (list): List to store the first detected target color
        stop_event (threading.Event): Event to signal when to stop rotation
    """
    # Open camera capture
    cap = cv2.VideoCapture(0)
    
    start_time = t.time()
    while t.time() - start_time < duration and not stop_event.is_set():
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        # Detect color boxes
        processed_frame, target_detected = detect_color_boxes(frame, target_colors, detected_colors, detected_target, stop_event)
        
        # Display the frame
        cv2.imshow('Color Detection (Center Region Focus)', processed_frame)
        
        # Break if key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Small delay to control loop rate
        t.sleep(0.1)
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

def run_detection_rotation(kobuki, duration, target_colors):
    """
    Run color detection and robot rotation in parallel, 
    stopping if any target color is detected in the center region
    
    Args:
        kobuki: Robot control object
        duration (float): Maximum rotation and detection duration in seconds
        target_colors (list): List of color names to detect ['red', 'blue', 'green', 'yellow']
    
    Returns:
        str or None: The first detected target color in center, or None if none detected
    """
    # Initialize detected colors and target
    detected_colors = {
        'red': [],
        'blue': [],
        'green': [],
        'yellow': []
    }
    detected_target = [None]  # Using a list to store the target for thread access
    stop_event = threading.Event()
    
    # Create threads for rotation and color detection
    rotation_thread = threading.Thread(target=rotate_robot, args=(kobuki, duration, stop_event))
    detection_thread = threading.Thread(target=detect_colors, args=(duration, target_colors, detected_colors, detected_target, stop_event))
    
    # Start both threads
    rotation_thread.start()
    detection_thread.start()
    
    # Wait for both threads to complete
    rotation_thread.join()
    detection_thread.join()
    
    # Return detected target color if any
    return detected_target[0]

def find_color_boxes(kobuki, target_colors, duration=30):
    """
    Rotate the robot and find specified color boxes in the center third of the view,
    stopping on first detection in the center region
    
    Parameters:
    - kobuki: Robot control object
    - target_colors: List of colors to look for ['red', 'blue', 'green', 'yellow']
    - duration: Maximum time to rotate and detect (default 30 seconds)
    
    Returns:
    - String name of the first detected target color in center, or None if none detected
    """
    detected_target = run_detection_rotation(kobuki, duration, target_colors)
    
    if detected_target:
        print(f"Successfully detected a {detected_target} box in the center region!")
        return detected_target
    else:
        print("No target colors detected in the center region during rotation.")
        return None