import os
import cv2
import numpy as np
import easyocr
import torch
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                image_files.append(os.path.join(root, file))
    return image_files

def add_noise(image, level=0.6):
    noise = np.zeros_like(image)
    height, width, channels = image.shape
    for i in range(height):
        for j in range(width):
            r = random.uniform(0, level)
            g = random.uniform(255, level)
            b = random.uniform(255, level)
            noise[i][j] = (r, g, b)
    return cv2.addWeighted(image, 1-level, noise, level, 0)

def desensitize_images(directory):
    image_files = get_image_files(directory)
    reader = easyocr.Reader(['en'])
    for i, file in enumerate(image_files):
        print(f'Processing image {i+1} of {len(image_files)}')
        image = cv2.imread(file)
        results = reader.readtext(file)
        for result in results:
            bbox = result[0]
            text = result[1]
            if bbox is not None:
                top_left, bottom_right = bbox[0], bbox[2]
                x1, y1 = int(top_left[0]), int(top_left[1])
                x2, y2 = int(bottom_right[0]), int(bottom_right[1])
                sub_image = image[y1:y2, x1:x2, :]
                sub_image = add_noise(sub_image)
                image[y1:y2, x1:x2, :] = sub_image
        # 将结果保存到新文件中
        new_file = file.replace(directory, directory + "_processed")
        os.makedirs(os.path.dirname(new_file), exist_ok=True)
        cv2.imwrite(new_file, image)



desensitize_images('Results') 
