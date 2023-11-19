from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import cv2
from io import BytesIO
# ddd
app = Flask(__name__)
CORS(app)

def predict_image(file):
    try:
        model = YOLO('C:/Users/Minchan/vscode-workplace/SkinCare/20231114data2.pt')
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
            cv2.rectangle(img_array, (xmin, ymin), (xmax,ymax), (0,255,0),2)
            cv2.putText(img_array, text, (xmin,ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.waitKey(0)
            cv2.imwrite("test.png", img_array)
            predictions.append({
                'image' : "test.png",
                'class': class_name,
                'confidence': round(conf, 2),
                'box': {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
            })

        return predictions

    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']

        # 이미지 예측
        predictions = predict_image(file)

        return jsonify({'result': predictions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
