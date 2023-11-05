import cv2
import numpy as np

def process_image(input_image):
    # 이미지를 그레이스케일로 변환 또는 원하는 처리 수행
    processed_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    return processed_image
