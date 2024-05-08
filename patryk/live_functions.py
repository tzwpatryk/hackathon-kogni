# import time
# import cv2
# from deepface import DeepFace
# #from GazeTracking.gaze_tracking import GazeTracking
# import os

# def get_frames():
#     camera = cv2.VideoCapture(0)
#     faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
#     while True:
#         ret, frame = camera.read()
#         try:
#             result = DeepFace.analyze(frame, actions=['emotion'])
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = faceCascade.detectMultiScale(gray, 1.1, 4)
#             if len(faces) > 1:
#                 faces = [max(faces, key=lambda rect: rect[2] * rect[3])]
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             cv2.putText(frame, 
#                         result[0]['dominant_emotion'], 
#                         (50, 50), 
#                         font, 3, 
#                         (0, 0, 255), 
#                         2, 
#                         cv2.LINE_4)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#         except ValueError:
#             pass

# def get_gaze(camera):
#     gaze = GazeTracking()

#     timeout = 10
#     start_time = time.time()

#     total_frames = 0
#     center_frames = 0

#     while True:
#         ret, frame = camera.read()
#         gaze.refresh(frame)

#         total_frames += 1

#         new_frame = gaze.annotated_frame()
#         text = ""

#         if gaze.is_right():
#             text = "Looking right"
#         elif gaze.is_left():
#             text = "Looking left"
#         elif gaze.is_center():
#             text = "Looking center"
#             center_frames += 1

#         cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        
#         ret, buffer = cv2.imencode('.jpg', new_frame)
#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
#         if time.time() > start_time + timeout:
#             camera.release()
#             break
    
#     with open('app/static/texts/gaze.txt', 'w') as f:
#         f.write(f'{center_frames/total_frames*100:.2f}%')
