def count_eggs(response):
    egg_counts = {}

    try:
        predictions = response
        for pred in predictions:
            label = pred.get('name')
            if label:
                if label not in egg_counts:
                    egg_counts[label] = 0
                egg_counts[label] += 1
    except Exception as e:
        print(f"Error processing response: {e}")

    return egg_counts

def process_egg_counts(response, frame):
    egg_counts = count_eggs(response)

    if sum(egg_counts.values()) == 4:
        quadrants = ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"]
        quadrant_labels = {q: [] for q in quadrants}

        width, height = frame.shape[1], frame.shape[0]

        for pred in response:
            x1, y1, x2, y2 = pred['box'].values()
            label = pred['name']

            x = (x1 + x2) / 2
            y = (y1 + y2) / 2

            if x < width / 2 and y < height / 2:
                quadrant_labels["Quadrant 1"].append(label)
            elif x >= width / 2 and y < height / 2:
                quadrant_labels["Quadrant 2"].append(label)
            elif x < width / 2 and y >= height / 2:
                quadrant_labels["Quadrant 3"].append(label)
            else:
                quadrant_labels["Quadrant 4"].append(label)

        all_quadrants_have_labels = True
        for q, labels in quadrant_labels.items():
            # print(f"{q}: {', '.join(labels) if labels else 'None'}")
            if not labels:
                all_quadrants_have_labels = False

        if all_quadrants_have_labels:
            print(response)
            print("\nEgg counts:", egg_counts, "\n")
            return True
        else:
            print("Not all quadrants have labels. Retaking the picture.\n")
            return False
    else:
        print("Egg count is not 4. Retaking the picture.\n")
        return False
