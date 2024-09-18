# ultralytics https://docs-ultralytics-com.translate.goog/modes/predict/?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=sc

from ultralytics import YOLO
from Quadrans import draw_quadrants
from Counting import process_egg_counts  
from Size import print_quadrants_with_diameters, annotate_frame_with_diameters
import supervision as sv
import cv2
import json

# Load the pre-trained YOLOv8n model
model = YOLO("model_1.pt")

# Open the video file
video_path = "C:\\Users\\Marsadinata\\Desktop\\Coding Skripsi\\Python\\myasset\\ECE_Video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

# Capture the original frame dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

original_width, original_height = frame.shape[1], frame.shape[0]

# Release the first frame as it's only used to get dimensions
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        print("End of video reached or error reading frame")
        break

    # Run inference on the captured frame using YOLO
    results = model.predict(frame, iou=0, agnostic_nms=True, save_txt=False)[0]

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
    display_frame = cv2.resize(annotated_frame, (1280, 720))  # Resize if needed for display purposes
    cv2.imshow('Video', display_frame)

    # Check for spacebar press to capture the image
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break 
    elif key == ord(' '):

        # Process the egg counts and check if egg counts is 4
        frame_captured = process_egg_counts(response, frame)

        if not frame_captured:
            continue

        # Get the output string for Arduino
        output_string = print_quadrants_with_diameters(response, frame)

        # Debug: Print the output string
        print("Output String for Arduino:\n", output_string)

        # Print the quadrants with labels and diameters
        print_quadrants_with_diameters(response, frame)
        break

# Release the video capture object
cap.release()

# Display the last annotated frame if it exists
if 'annotated_frame' in locals():
    display_frame = cv2.resize(annotated_frame, (640, 480))  # Resize if needed for display purposes
    cv2.imshow('Image with Annotations', display_frame)

    # Wait for a key press to close the window
    cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
