from flask import Flask, render_template, request
from PIL import Image
from collections import Counter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_most_common_colors(image_path, num_colors=5):
    with Image.open(image_path) as img:
        img = img.resize((100, 100))  # Resize for faster processing
        pixels = img.getdata()
        pixels = [pixel[:3] for pixel in pixels]  # Ignore alpha channel if present
        color_counts = Counter(pixels)
        most_common_colors = color_counts.most_common(num_colors)
        return most_common_colors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        common_colors = get_most_common_colors(filepath)
        return render_template('result.html', common_colors=common_colors, image_path=filepath)

if __name__ == '__main__':
    app.run(debug=True)
