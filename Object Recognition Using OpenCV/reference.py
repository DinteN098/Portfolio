import cv2
import numpy as np
import time

# Load the pre-trained MobileNet SSD model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

# Initialize a dictionary to keep track of the time a person enters the blue rectangle
person_time = {}
person_centroid = {}

def detect_people(frame):
    h, w = frame.shape[:2] #frame.shape is a tuple that contains h and w like this (h , w)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5) #turn to blob
    net.setInput(blob) #sends information to neural network
    detections = net.forward() #runs the detection of objects
    
    people = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            if idx == 15:  # Class ID for person in MobileNetSSD
                #we multiply the detection coordinates by the frame dimensions
                #example box = np.array([0.1, 0.2, 0.3, 0.4]) * np.array([640, 480, 640, 480])
                #box = np.array([64, 96, 192, 192])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                #we turn the numpy array values from box to integers and assign it to values
                (startX, startY, endX, endY) = box.astype("int")

                #we then append the coordinates where the object (person) is and add it to the people list
                people.append((startX, startY, endX, endY))
    return people


def calculate_centroid(startX, startY, endX, endY):
    return (startX + endX) // 2, (startY + endY) // 2

# Initialize the video capture
cap = cv2.VideoCapture('test videos/2048246-hd_1920_1080_24fps.mp4')

a = cap
while True:
    #cap.read() has a boolean value and a numpy array, we assign
    #the boolean to ret and the numpy array to frame
    
    #
    ret, frame = cap.read()
    if not ret:
        break
    
    #frames hight and width 
    h, w = frame.shape[:2] 
    middle_frame = (w // 4, h // 4, w * 3 // 4, h * 3 // 4)
    #rectangle drawn where people should be             (coordinates1, coordinates2, coordinates3, coordinates4, colorsBGR, thickness)
    cv2.rectangle(frame, (middle_frame[0], middle_frame[1]), (middle_frame[2], middle_frame[3]), (255, 0, 0), 2)

    #variable holding detected people
    people = detect_people(frame)
    
    #starting timer for when person shows inside the rectangle
    current_time = time.time()

    #remembering the person inside the rectangle time and center
    new_person_time = {}
    new_person_centroid = {}

    #for every person's coordinates
    for (startX, startY, endX, endY) in people:

        #we calculate the center x and y
        centerX, centerY = calculate_centroid(startX, startY, endX, endY)
        
        # Determine if the person is inside the blue rectangle
        if middle_frame[0] < centerX < middle_frame[2] and middle_frame[1] < centerY < middle_frame[3]:

            min_dist = float('inf')

            closest_person_id = None

            #for every person's center x and y in the people's previous centroids
            for person_id, (cx, cy) in person_centroid.items():

                #we calculate their distances
                dist = (centerX - cx) ** 2 + (centerY - cy) ** 2

                #if the current distance is smaller than the min distance
                if dist < min_dist:
                    #update the min distance
                    min_dist = dist

                    #we update the closest person id to the current person
                    closest_person_id = person_id

            #if the person is still in the rectangle and it's min distance is less that 50**2
            #we do 50**2 because it represents a squared distance, a person is considered to be the same
            #if their centroid is withing the distance of 50 pixels from a previous tracked centroid
            if closest_person_id is not None and min_dist < 50 ** 2:
                #we assign the previous time from before and assign it to new_person_time
                new_person_time[closest_person_id] = person_time[closest_person_id]
                #we update their centroids
                new_person_centroid[closest_person_id] = (centerX, centerY)
                #we update the current time
                elapsed_time = current_time - new_person_time[closest_person_id]
                #we then show the elapsed time in a text in top of the person
                cv2.putText(frame, f"Time: {elapsed_time:.2f}s", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                #else if the centroid is not close enough to any tracked centroids meaning is a new person 
                #we create a new person id
                person_id = len(person_time) + 1
                #we assign it the current time
                new_person_time[person_id] = current_time
                #we initialize its centroids
                new_person_centroid[person_id] = (centerX, centerY)
        else:
            #else if the person is outside the rectangle
            if person_id in person_time:
                #delete times and centroids
                del person_time[person_id]
                del person_centroid[person_id]

        #we have a rectangle that will show where the detected person is
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

    # Update the person_time and person_centroid dictionaries
    person_time = new_person_time
    person_centroid = new_person_centroid

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
