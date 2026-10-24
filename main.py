from flask import Flask, render_template, request, send_from_directory, Response, send_file
import os
import cv2
from PIL import Image
import io
from ultralytics import YOLO  
import argparse
import time

# Initialization of the Flask app
app = Flask(__name__)

# code to render the home page
@app.route("/")
def hello_world():
    return render_template('index.html')

# code for handling image upload and object detection
@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST" and 'file' in request.files:
        f = request.files['file']                                        # Get the uploaded file
        basepath = os.path.dirname(__file__)                             # Get the base directory path
        filepath = os.path.join(basepath, 'uploads/images', f.filename)  # Define file save path
        print("Upload folder is ", filepath)
        f.save(filepath)                                                 # Save the uploaded file to the specified path

        # check if it's a valid image
        file_extension = f.filename.rsplit('.', 1)[1].lower()
        if file_extension == 'jpg':
            img = cv2.imread(filepath)                                   # Read image using OpenCV
            frame = cv2.imencode('.jpg', cv2.UMat(img))[1].tobytes()     # Convert image to bytes for further processing
            image = Image.open(io.BytesIO(frame))
            model = YOLO("weights/best.pt", "v8")                        # Load YOLO model for object detection
            detection_output = model.predict(source=img, conf=0.25, save=True)  # Perform detection
            
            return display(f.filename)                                   # Return the detected image

        else:
            return "Invalid file format"

    # Fetch the latest detected image from the 'runs/detect' directory
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    image_path = folder_path + '/' + latest_subfolder + '/' + f.filename

    # Render the template with the detected image
    return render_template('index.html', image_path=image_path)


# Route to display the processed image
@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = folder_path + '/' + latest_subfolder
    print("Printing directory:", directory)
    files = os.listdir(directory)
    latest_file = files[0]
    print(latest_file)
    filename = os.path.join(folder_path, latest_subfolder, latest_file)
    file_extension = filename.rsplit('.', 1)[1].lower()
    if file_extension == 'jpg':
        return send_from_directory(directory, latest_file)  
    else:
        return "Invalid file format"

# Main entry point for running the Flask app
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing YOLOv8 models")
    parser.add_argument("--port", default=5000, type=int, help="Port number")
    args = parser.parse_args()

    app.run(port=args.port)
