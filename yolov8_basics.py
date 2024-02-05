from ultralytics import YOLO
import numpy


model = YOLO("weights/best.pt", "v8")  

# predict on an image
detection_output = model.predict(source="inference/images/image2.jpg", conf=0.25, save=True) 

# Display tensor array
print(detection_output)

# Display numpy array
print(detection_output[0].numpy())
