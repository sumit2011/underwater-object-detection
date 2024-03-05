from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
from flask import redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads2'
ANNOTATION_FOLDER = 'annotations'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANNOTATION_FOLDER'] = ANNOTATION_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('annotate.html')


        
@app.route('/upload', methods=['POST'])
def upload():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
        
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = file.filename
        # image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        basepath = os.path.dirname(__file__)
        image_path = os.path.join(basepath, 'uploads2', file.filename)

        file.save(image_path)
        print("Image saved at:", image_path) 
        # return jsonify({'success': True})
        return render_template('alert.html', message='Image uploaded successfully!')
    
    return jsonify({'error': 'Invalid file format'})


main_app_directory = os.path.dirname(os.path.abspath(__file__))
annotations_directory = os.path.join(main_app_directory, ANNOTATION_FOLDER)



@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    annotation = request.json
    image_filename = annotation['image_filename']
    annotation_data = annotation['annotation']
    # Save annotation data to a file in YOLO format
    yolo_filename = os.path.join(annotations_directory, os.path.splitext(os.path.basename(image_filename))[0] + '.txt')
    print("Annotation saved at:", yolo_filename)
    with open(yolo_filename, 'w') as f:
        for ann in annotation_data:
            x_center = (ann['left'] + ann['width'] / 2) / ann['img_width']
            y_center = (ann['top'] + ann['height'] / 2) / ann['img_height']
            width = ann['width'] / ann['img_width']
            height = ann['height'] / ann['img_height']
            line = f"{ann['class_id']} {x_center} {y_center} {width} {height}\n"
            f.write(line)
            
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)


