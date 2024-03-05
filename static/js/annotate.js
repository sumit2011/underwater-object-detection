var canvas = new fabric.Canvas('canvas');
var uploadedImage;
var isDrawingMode = false;
var imageFilename = null;  
var classIds = []; 

function uploadImage() {
  var input = document.getElementById('imageUploadInput');
  if (!input.files || !input.files[0]) {
    alert('Please select an image file.');
    return;
  }
  
  var file = input.files[0];
  var reader = new FileReader();
  
  reader.onload = function(event) {
    var imageUrl = event.target.result;
    imageFilename = file.name;  
    loadImageToCanvas(imageUrl);
  };
  
  reader.readAsDataURL(file);
}


function loadImageToCanvas(imageUrl) {
  fabric.Image.fromURL(imageUrl, function(img) {
    uploadedImage = img;
    uploadedImage.scaleToWidth(canvas.width);
    uploadedImage.scaleToHeight(canvas.height);
    canvas.setBackgroundImage(uploadedImage, canvas.renderAll.bind(canvas), {
      crossOrigin: 'anonymous',
      scaleX: canvas.width / uploadedImage.width,
      scaleY: canvas.height / uploadedImage.height
    });
  });
}

function enableDrawing() {
  isDrawingMode = !isDrawingMode;
  canvas.isDrawingMode = false; 
  canvas.selection = !isDrawingMode;
  canvas.forEachObject(function(obj) {
    obj.selectable = !isDrawingMode;
  });

  if (!isDrawingMode) {
    canvas.off('mouse:down');
    canvas.off('mouse:move');
    canvas.off('mouse:up');
  } else {
    canvas.on('mouse:down', startDrawing);
  }
}

function startDrawing(event) {
  var pointer = canvas.getPointer(event.e);
  var rect = new fabric.Rect({
    left: pointer.x,
    top: pointer.y,
    width: 0,
    height: 0,
    fill: 'transparent',
    stroke: 'red',
    strokeWidth: 2
  });
  canvas.add(rect);
  canvas.setActiveObject(rect);
  canvas.renderAll();

  canvas.off('mouse:down');
  canvas.on('mouse:move', resizeRectangle);
  canvas.on('mouse:up', stopDrawing);
}

function resizeRectangle(event) {
  var pointer = canvas.getPointer(event.e);
  var activeObject = canvas.getActiveObject();
  activeObject.set({
    width: Math.abs(pointer.x - activeObject.left),
    height: Math.abs(pointer.y - activeObject.top)
  });
  canvas.renderAll();
}

function stopDrawing() {
  canvas.getActiveObject().setCoords();
  canvas.renderAll();
  classIds.push(document.getElementById('classId').value); 
  enableDrawing();
}

document.getElementById('saveAnnotation').addEventListener('click', function() {
    if (uploadedImage && imageFilename) {   
        var objects = canvas.getObjects().map((obj, index) => {
            var rect = obj.aCoords;
            return {
                class_id: classIds[index], 
                img_width: uploadedImage.width,
                img_height: uploadedImage.height,
                left: rect.bl.x,
                top: rect.tl.y,
                width: rect.tr.x - rect.tl.x,
                height: rect.bl.y - rect.tl.y
            };
        });

        var annotation = {
            image_filename: imageFilename,   
            annotation: objects
        };

        fetch('/save_annotation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(annotation)
        })
        .then(response => response.json())
        .then(data => {
            alert('Annotation saved successfully.');
            classIds = []; 
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
    }
});

// Keyboard listener to delete selected rectangle when "Delete" key is pressed
document.addEventListener('keydown', function(event) {
  if ((event.key === 'Delete' || event.key === 'Backspace') && !isDrawingMode) {
    var activeObject = canvas.getActiveObject();
    if (activeObject && activeObject.type === 'rect') {
      canvas.remove(activeObject);
      canvas.renderAll();
    }
  }
});
