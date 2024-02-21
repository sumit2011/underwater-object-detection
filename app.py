from flask import Flask, render_template, request, send_from_directory, Response, send_file
import os
import cv2
from PIL import Image
import io
from ultralytics import YOLO  
import argparse
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')





@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST" and 'file' in request.files:
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads/images', f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)

        file_extension = f.filename.rsplit('.', 1)[1].lower()
        if file_extension == 'jpg':
            img = cv2.imread(filepath)
            frame = cv2.imencode('.jpg', cv2.UMat(img))[1].tobytes()
            image = Image.open(io.BytesIO(frame))
            model = YOLO("weights/best.pt", "v8")  
            detection_output = model.predict(source=img, conf=0.25, save=True) 
            # yolo = YOLO('best.pt')
            # detections = yolo.predict(image, save=True)
            return send_from_directory('runs/detect', f.filename)
            # return send_file(os.path.join('runs/detect', f.filename), mimetype='image/jpg')
            # return send_from_directory('runs/detect', detection_output)
        else:
            return "Invalid file format"
        

        
# @app.route('/<path:filename>')
# def display(filename):
#     folder_path = 'runs/detect'
#     subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
#     latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
#     directory = folder_path+'/'+latest_subfolder
#     print("printing directory: ",directory)  
#     file_extension = filename.rsplit('.', 1)[1].lower()
#     print("printing file extension from display function : ",file_extension)
#     environ = request.environ
#     if file_extension == 'jpg':      
#         return send_from_directory(directory,filename,environ)
#     else:
#         return "Invalid file format"
    
@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = folder_path+'/'+latest_subfolder
    print("printing directory: ", directory)
    files = os.listdir(directory)
    latest_file = files[0]
    print(latest_file)
    filename = os.path.join(folder_path, latest_subfolder, latest_file)
    file_extension = filename.rsplit('.', 1)[1].lower()
    if file_extension == 'jpg':
        return send_from_directory(directory, latest_file)  # shows the result in separate tab
    else:
        return "Invalid file format"



# @app.route('/<path:filename>')
# def display_latest_image(filename):
#     folder_path = 'runs/detect'

#     # Get the latest subfolder in the specified directory
#     subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
#     if not subfolders:
#         return "No subfolders found", 404

#     latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
#     directory = os.path.join(folder_path, latest_subfolder)

#     # Get the latest file in the latest subfolder
#     files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#     if not files:
#         return "No files found", 404

#     latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(directory, x)))

#     # Check if the latest file is a JPG
#     file_extension = latest_file.rsplit('.', 1)[-1].lower()
#     if file_extension == 'jpg':
#         image_path = os.path.join(directory, latest_file)
#         return render_template('display_image.html', image_path=image_path)
#     else:
#         return "Invalid file format", 400




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov8 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(port=args.port)

