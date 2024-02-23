# Underwater-Object-Detection using YOLOv8.1
![image](static/images/1.png)  

<p>
The Underwater Object Detection WebApp is an intuitive online tool tailored for marine researchers, underwater explorers, and defense personnel. It employs advanced sonar technology and image processing algorithms to analyze uploaded sonar data or underwater images from ROVs and cameras. Users can detect and classify submerged objects such as wreckage or marine life, visualize results through interactive maps or image galleries, and access features like object tracking and measurement tools. With its user-friendly interface and powerful capabilities, the web app facilitates efficient underwater exploration, environmental monitoring, and maritime security efforts.
</p>

## Step 1:
### Clone the repository.
```bash
git clone https://github.com/sumit2011/underwater-object-detection
```

## Step 2:
> for linux
### Create virtual environment.
```bash
virtualenv myenv
```
### Activate virtual environment.
```bash
source myenv/bin/activate
```


## Step 3:
### Installing require modules.
```bash
pip install -r requirements.txt
```

## Step 4:
### Run the script.
```bash
python -u app.py
```
## Step 5:
### open the link 


## log output
```python
┌──(yoloenv)─(sumit㉿mr-nob0dy)-[~/Desktop/underwater_object_detection]
└─$ python -u "/home/sumit/Desktop/underwater_object_detection/app.py"
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [23/Feb/2024 21:10:14] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Feb/2024 21:10:14] "GET /static/images/house-solid.svg HTTP/1.1" 304 -
127.0.0.1 - - [23/Feb/2024 21:10:14] "GET /static/styles/style.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Feb/2024 21:10:14] "GET /static/images/github.svg HTTP/1.1" 304 -
upload folder is  /home/sumit/Desktop/underwater_object_detection/uploads/images/image7.jpg

0: 800x608 15 jellyfishs, 243.0ms
Speed: 6.0ms preprocess, 243.0ms inference, 0.9ms postprocess per image at shape (1, 3, 800, 608)
Results saved to runs/detect/predict5
printing directory:  runs/detect/predict5
image0.jpg
127.0.0.1 - - [23/Feb/2024 21:10:28] "POST / HTTP/1.1" 200 -
```



