def main():
    # Imports as mentioned
    from kobukidriversample import Kobuki
    import movement
    import navigate
    import colordetectionwhilerotatng
    
    # Color sequence to follow
    color_sequence = ['red', 'blue', 'green', 'yellow']
    
    # Initialize Kobuki robot
    kobuki = Kobuki()
    
    # Robot navigation parameters
    y_center = 240  # Center position of horizontal lines (vertical)
    gap = 50        # Gap between horizontal lines in pixels
    forward_speed = 150  # Forward movement speed
    
    # Keep track of which colors we've already processed
    processed_colors = []
    
    # Main loop - continue until all colors have been processed
    while len(processed_colors) < len(color_sequence):
        # First, navigate using white line detection to search for boxes
        print("hello world")
        navigate.robot_navigation(
            kobuki=kobuki,
            color="white",
            y_center=y_center,
            gap=gap,
            forward_speed=forward_speed
        )
        
        # Start rotating to detect any available color box
        # We'll try to detect any color in our sequence that hasn't been processed yet
        remaining_colors = [color for color in color_sequence if color not in processed_colors]
        
        detected_color = None
        
        # Rotate and detect color
        detected_color = colordetectionwhilerotatng.find_color_boxes(
            kobuki, 
            remaining_colors, 
            100
        )
        print(f"Detected color: {detected_color}")


        # If no color was detected, rotate and try again
        if not detected_color:
            # Rotate and detect color
            detected_color = colordetectionwhilerotatng.find_color_boxes(
                kobuki, 
                remaining_colors, 
                100
            )
            continue
        
        # Navigate to the detected color box
        navigate.robot_navigation(
            kobuki=kobuki,
            color=detected_color,
            y_center=y_center,
            gap=gap,
            forward_speed=forward_speed
        )
        
        
        # Navigate to the detected color box
        navigate.robot_navigation(
            kobuki=kobuki,
            color=detected_color,
            y_center=y_center,
            gap=gap,
            forward_speed=forward_speed
        )
        
        #move backward
        movement.move_backward(kobuki,forward_speed)
        # Rotate to find a cell of the destination color

        destination_color = ["white"]

        cell_detected = colordetectionwhilerotatng.find_color_boxes(
            kobuki, 
            destination_color,
            100
        )
        
        
        
        # Mark this color as processed
        processed_colors.append(detected_color)
        print(f"Placed {detected_color} box. Processed colors: {processed_colors}")
            
        # Continue searching for remaining colors
    
    # After all colors are processed
    movement.stop(kobuki)  # Stop the robot
    print("Task completed. All boxes placed:", processed_colors)

if __name__ == "__main__":
    main()