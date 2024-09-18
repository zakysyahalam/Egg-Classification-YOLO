from ultralytics import YOLO
from Quadrans import draw_quadrants
from Counting import process_egg_counts  
from Size import print_quadrants_with_diameters, annotate_frame_with_diameters
import supervision as sv
import cv2
import json
import serial
import time  # To add a delay

# Set up the serial connection to Arduino
port_var = "COM5"
serial_inst = serial.Serial(port=port_var, baudrate=9600, timeout=1)

# Load the pre-trained YOLOv8n model
model = YOLO("model_4.pt")

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Set the resolution to 1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Initialize flag
frame_captured = False

while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam")
        break

    # Run inference on the captured frame using YOLO
    results = model.predict(frame, iou=0, agnostic_nms=True)[0]

    # Convert results to supervision detections
    detections = sv.Detections.from_ultralytics(results)

    # Create supervision annotators
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # Chain annotate the image with our inference results
    annotated_frame = box_annotator.annotate(scene=frame, detections=detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections)

    # Convert results to JSON and then to a Python list of dictionaries
    response_json = results.tojson()
    response = json.loads(response_json)  # Convert JSON string to Python object

    # Annotate the frame with bounding boxes and diameters
    annotate_frame_with_diameters(response, annotated_frame)

    # Draw quadrants and labels using the imported function
    draw_quadrants(annotated_frame)

    # Display the frame (resize for display if needed)
    display_frame = cv2.resize(annotated_frame, (640, 480))  # Resize for display purposes
    # cv2.imshow('Webcam', display_frame)

    # Wait for 3 seconds before simulating a spacebar press
    time.sleep(3)  # Wait for 3 seconds
    key = ord(' ')  # Automatically set key to 'space' after 3 seconds

    if key == 27:  # ESC key
        break 
    elif key == ord(' '):
        # Process the egg counts and check if egg count is 4
        frame_captured = process_egg_counts(response, frame)
        if not frame_captured:
            continue

        # Get the output string for Arduino
        output_string = print_quadrants_with_diameters(response, frame)

        # Debug: Print the output string
        print("Output String for Arduino:\n", output_string)

        # Send the output string to Arduino
        try:
            serial_inst.write(output_string.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")

        break

# Release the webcam and close serial port
cap.release()
serial_inst.close()

# Display the last annotated frame if it exists
if 'annotated_frame' in locals():
    display_frame = cv2.resize(annotated_frame, (640, 480))  # Resize for display purposes
    cv2.imshow('Image with Annotations', display_frame)

    # Wait for a key press to close the window
    cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
