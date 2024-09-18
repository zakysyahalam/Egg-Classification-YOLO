import cv2

def convert_to_cm(pixels, dpi=170):  # DPI is set to 170 after comparing the predict and actual result
    inches = pixels / dpi
    cm = inches * 2.54
    return cm

def measure_egg_diameter(predictions):
    egg_diameters = []

    for pred in predictions:
        width = pred['box']['x2'] - pred['box']['x1']
        height = pred['box']['y2'] - pred['box']['y1']
        diameter = min(width, height)
        diameter_cm = convert_to_cm(diameter)
        egg_diameters.append(diameter_cm)

    return egg_diameters

def annotate_frame_with_diameters(response, frame):
    egg_diameters = measure_egg_diameter(response)

    for pred in response:
        x1, y1 = pred['box']['x1'], pred['box']['y1']
        x2, y2 = pred['box']['x2'], pred['box']['y2']
        diameter = egg_diameters.pop(0)

        # Calculate the center of the bounding box
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        # Calculate the size of the text to adjust its position
        text = f'{diameter:.2f} cm'
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        text_x = center_x - text_width // 2
        text_y = center_y + text_height // 2

        # Draw the diameter at the center of the bounding box
        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2
        )

def print_quadrants_with_diameters(response, frame):
    egg_diameters = measure_egg_diameter(response)
    quadrants = ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"]
    width, height = frame.shape[1], frame.shape[0]
    quadrant_labels = {q: [] for q in quadrants}

    for pred in response:
        x1, y1, x2, y2 = pred['box'].values()
        label = pred['name']
        diameter = egg_diameters.pop(0)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        if x < width / 2 and y < height / 2:
            quadrant_labels["Quadrant 1"].append((label, diameter))
        elif x >= width / 2 and y < height / 2:
            quadrant_labels["Quadrant 2"].append((label, diameter))
        elif x < width / 2 and y >= height / 2:
            quadrant_labels["Quadrant 3"].append((label, diameter))
        else:
            quadrant_labels["Quadrant 4"].append((label, diameter))

    output = ""
    for q, labels in quadrant_labels.items():
        output += f"{q}: {','.join([f'{label} | Diameter = {diameter:.2f} cm' for label, diameter in labels]) if labels else 'None'}\n"
    return output
