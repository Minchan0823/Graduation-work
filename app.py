from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import cv2
from io import BytesIO
import base64
import os

app = Flask(__name__)
CORS(app)

app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

def predict_image(file):
    try:
        model = YOLO('../1114data2.pt')
        image = Image.open(file)
        results = model(image)
        img_array = results[0].orig_img
        predictions = []

        bndboxs = results[0].boxes.data
        names = results[0].names

        for i, bndbox in enumerate(bndboxs):
            xmin = int(bndbox[0])
            ymin = int(bndbox[1])
            xmax = int(bndbox[2])
            ymax = int(bndbox[3])
            conf = float(bndbox[4])
            class_id = int(bndbox[5])
            class_name = names[class_id]

            text = f"{class_name}-{round(conf, 2)}"
            print(text)
            cv2.rectangle(img_array, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(img_array, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.waitKey(0)
            # 예측된 이미지를 Base64로 인코딩
            _, img_encoded = cv2.imencode('.png', img_array)
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

            predictions.append({
                'image': img_base64,
                'class': class_name,
                'confidence': round(conf, 2),
                'box': {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
            })

        return predictions

    except Exception as e:
        return str(e)

# 정적 파일 (이미지)을 서빙하기 위한 코드 추가
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        predictions = predict_image(file)
        return jsonify({'result': predictions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

