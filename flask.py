from flask import Flask, jsonify
import os

app = Flask(__name__)

# Папка для хранения изображений
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# API для получения списка изображений
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    images = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.png'):
            images.append({
                "url": f"/{UPLOAD_FOLDER}/{filename}"
            })
    return jsonify(images)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)