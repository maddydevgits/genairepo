import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Set the video output parameters
output_path = 'output_gesture_video.avi'
frame_width = 640
frame_height = 480
fps = 24

# Initialize webcam or provide the path to your video file
video_source = 0  # Use 0 for webcam, or specify the path to your video file
cap = cv2.VideoCapture(video_source)

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Initialize hand tracking
with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
                data = [normalized_landmark.x for normalized_landmark in hand_landmarks.landmark]
                data = ",".join(map(str, data))
                print(data)

                # Write frame to video file
                out.write(image)

        cv2.imshow('Hand Tracking', image)
        
        if cv2.waitKey(20) & 0xFF == 27:
            break

# Release video writer and capture
out.release()
cap.release()
cv2.destroyAllWindows()
