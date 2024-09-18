import cv2

def draw_quadrants(frame):
    # Draw horizontal and vertical lines
    height, width = frame.shape[:2]
    cv2.line(frame, (width // 2, 0), (width // 2, height), (102, 255, 204), 2)  # Vertical line
    cv2.line(frame, (0, height // 2), (width, height // 2), (102, 255, 204), 2)  # Horizontal line

    # Define quadrant centers
    quadrant_centers = [
        (width // 4, height // 4),             # Quadrant I
        (3 * width // 4, height // 4),         # Quadrant II
        (width // 4, 3 * height // 4),         # Quadrant III
        (3 * width // 4, 3 * height // 4)      # Quadrant IV
    ]

    # Define quadrant labels
    quadrant_labels = ["I", "II", "III", "IV"]

    # Draw labels
    for center, label in zip(quadrant_centers, quadrant_labels):
        cv2.putText(
            frame,
            label,
            center,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

