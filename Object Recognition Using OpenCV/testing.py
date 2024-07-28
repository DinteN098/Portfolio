import cv2
import numpy as np
import time

#loading a pre-trained deep neural network (MobileNet SSD) for object detection using cv2.dnn.
#from cv2 deep neural network use readNetFromCaffe to read from the pre-trained data
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')


def detect_people(frame):
    #takes the height and width of the input frame
    #frame.shape gives a tuple with the dimensions from frame
    #we take the two elements from the tuple which are h and w
    h, w = frame.shape[:2]

    #blob means binary large object that represents an image in  a structured format for neural network precoesing
    #we resize the frame to 300x300. it then is converted to a format for a deep learning model by using 0.007843, (300, 300), 127.5)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    
    #used to set the input from blob for a pre-trained neural network
    #it prepares the neural network to receive and process input data in the form of a blob
    net.setInput(blob)

    #it instructs the neural network to process the input data 
    detections = net.forward()

    #a list that will keep track of the people that are on the camera
    people = []

    #iterates through all detections made by the neural network
    #detections includes information about each detected object in the input image
    #the attribute 'shape' gives the dimensions of the array
    #[0] num of images in the batch, [1], num of detection outputs, [2] num of detected objects
    #[3] info for each detection
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            if idx == 15:  # Class ID for person in MobileNetSSD
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                people.append((startX, startY, endX, endY))
    return people

# Initialize the video capture
cap = cv2.VideoCapture(0)

#while loop that processes video frames

while True:
    #ret is a boolean that indicates if the frame was successfully read
    #frame contains the captured image
    #if ret is False then the loop breaks
    ret, frame = cap.read()
    if not ret:
        break

    #defining a middle rectangle in the Frame
    h, w = frame.shape[:2]
    #middle_frame is a tuple defining a rectangle in the center of the frame (one-fourth of the width and height from each side)
    middle_frame = (w//4, h // 4, w * 3 // 4, h * 3 // 4)

    #drawing the middle blue rectangle on the frame
    cv2.rectangle(frame, (middle_frame[0], middle_frame[1]), (middle_frame[2], middle_frame[3]), (255, 0, 0), 2)

    #displaying processed frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
