import csv
import os
import ocr_three
import requests
import cv2
import numpy as np
from django.shortcuts import render
from flask import Flask, request, jsonify
from PIL import Image
from .utils import process_image

image_folder = 'uploads/' #실제 이미지 폴더 경로

# 폴더 내의 각 이미지 파일에 대해 처리
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg'):  # 확장자가 .jpg인 파일만 처리
        image_path = os.path.join(image_folder, filename)
        image = Image.open(image_path)

        result = ocr_three.process_and_save_image(image)

        result.show()


def read_text_to_blur_from_csv(csv_file):
    text_to_blur = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                words = row[0].split()  # 단어 단위로 분할
                text_to_blur.extend(words)  # 단어를 리스트에 추가
    return text_to_blur

# API 엔드포인트와 업로드할 이미지 파일 경로 설정
url = 'http://localhost:5000/process_image'
image_file_path = 'new_project/media/uploads'

# 이미지 파일 업로드
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg'):
        image_path = os.path.join(image_folder, filename)
        files = {'image': open(image_path, 'rb')}
        response = requests.post(url, files=files)

        # 결과 확인
        print(response.json())

#API 엔드포인트 설정
#이미지 처리 함수
def process_image(image_path):
    #이미지 로드
    img = cv2.imread(image_path)
    # 이미지 저장 경로 설정
    processed_image_path = 'output_folder/'  # 실제 경로로 대체해야 합니다.
    cv2.imwrite(processed_image_path, img)
    return processed_image_path

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image_endpoint():
    # 이미지 파일 받기
    image_file = request.files['image']
    image_path = os.path.join('uploads', image_file.filename)  # 실제 경로로 대체해야 합니다.
    image_file.save(image_path)

    # 이미지 처리
    processed_image_path = process_image(image_path)

    # 처리된 이미지를 클라이언트에게 반환
    processed_image = Image.open(processed_image_path)
    return jsonify({'processed_image_url': processed_image_path})

if __name__ == '__main__':
    app.run(debug=True)
