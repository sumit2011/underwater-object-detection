from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
from flask import redirect, url_for

app = Flask(__name__)

# Define directories for uploads and annotations
UPLOAD_FOLDER = 'uploads2'
ANNOTATION_FOLDER = 'annotations'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Allowed image file formats

# Configure Flask app with upload and annotation folder paths
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANNOTATION_FOLDER'] = ANNOTATION_FOLDER

# Function to check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page (renders annotation UI)
@app.route('/')
def index():
    return render_template('annotate.html')

# Route for uploading images
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})  # No file provided in the request

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})  # File name is empty

    if file and allowed_file(file.filename):
        filename = file.filename
        basepath = os.path.dirname(__file__)  # Get the base directory path
        image_path = os.path.join(basepath, 'uploads2', file.filename)  # Define file save path

        file.save(image_path)  # Save the uploaded file
        print("Image saved at:", image_path) 

        # Return success message and render an alert template
        return render_template('alert.html', message='Image uploaded successfully!')
    
    return jsonify({'error': 'Invalid file format'})  # File format not supported

# Define main application directory and annotation directory path
main_app_directory = os.path.dirname(os.path.abspath(__file__))
annotations_directory = os.path.join(main_app_directory, ANNOTATION_FOLDER)

# Route to save image annotations in YOLO format
@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    annotation = request.json  # Get JSON annotation data from request
    image_filename = annotation['image_filename']  # Extract image filename
    annotation_data = annotation['annotation']  # Extract annotation details

    # Define YOLO annotation file path
    yolo_filename = os.path.join(annotations_directory, os.path.splitext(os.path.basename(image_filename))[0] + '.txt')
    print("Annotation saved at:", yolo_filename)

    # Save annotation data in YOLO format
    with open(yolo_filename, 'w') as f:
        for ann in annotation_data:
            # Normalize coordinates for YOLO format
            x_center = (ann['left'] + ann['width'] / 2) / ann['img_width']
            y_center = (ann['top'] + ann['height'] / 2) / ann['img_height']
            width = ann['width'] / ann['img_width']
            height = ann['height'] / ann['img_height']
            
            # Write annotation to file in YOLO format: class_id x_center y_center width height
            line = f"{ann['class_id']} {x_center} {y_center} {width} {height}\n"
            f.write(line)
            
    return jsonify({'success': True})  

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
