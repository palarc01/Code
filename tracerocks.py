import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 1. Load the image
image_path = 'rocks.jpg'  # ← Change this to your image filename
original = cv2.imread(image_path)
original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

# 2. Setup to collect polygon points
selected_points = []
cropped_images = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))
        cv2.circle(display_image, (x, y), 3, (0, 255, 0), -1)

# 3. Main loop to extract rocks
rock_count = 0
while True:
    display_image = original.copy()
    selected_points = []

    cv2.namedWindow("Select Rock (Click around it, press 'c' to confirm)", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select Rock (Click around it, press 'c' to confirm)", click_event)

    while True:
        cv2.imshow("Select Rock (Click around it, press 'c' to confirm)", display_image)
        key = cv2.waitKey(1)

        if key == ord('c') and len(selected_points) >= 3:
            break
        elif key == ord('q'):
            cv2.destroyAllWindows()
            break

    if len(selected_points) < 3:
        break

    # 4. Create mask and crop rock
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    points_array = np.array([selected_points], dtype=np.int32)
    cv2.fillPoly(mask, points_array, 255)

    rock = cv2.bitwise_and(original, original, mask=mask)

    # Transparent background (optional)
    bgra = cv2.cvtColor(rock, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = mask

    # Crop bounding box
    x, y, w, h = cv2.boundingRect(points_array[0])
    cropped = bgra[y:y+h, x:x+w]

    # Save rock image
    rock_filename = f'rock_{rock_count}.png'
    cv2.imwrite(rock_filename, cropped)
    print(f'Saved {rock_filename}')
    cropped_images.append(rock_filename)
    rock_count += 1

    key = input("Press Enter to select another rock, or type 'done' to finish: ")
    if key.lower() == 'done':
        break

cv2.destroyAllWindows()

print("\nDone extracting rocks.")
