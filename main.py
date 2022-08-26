import time
import cv2
import numpy as np
import mediapipe as mp
import os

def main():
  mp_holistic = mp.solutions.holistic  # Holistic model
  mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
    
  def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                   # Image is no longer writeable
    results = model.process(image)                  # Make prediction
    image.flags.writeable = True                    # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results

  def draw_styled_landmarks(image, results):
    # Draw left hand
    mp_drawing.draw_landmarks(
      image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
      mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
      mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
    ) 
    # Draw right hand
    mp_drawing.draw_landmarks(
      image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
      mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
      mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    )
  
  def extract_keypoints(results):
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([lh, rh])
  
  cap = cv2.VideoCapture(0)
  # Set mediapipe model 
  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
      # Read feed
      ret, frame = cap.read()

      # Make detections
      image, results = mediapipe_detection(frame, holistic)
      
      # Draw landmarks
      draw_styled_landmarks(image, results)

      # Show to screen
      cv2.imshow('LSV Traductor', image)

      # Break gracefully
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()

# TODO: separar a otro archivo
def generate_data():
  # Path for exported data, numpy arrays
  DATA_PATH = os.path.join('data') 

  # Actions that we try to detect
  signs = np.array(['a', 'b', 'c', 'd', 'e'])

  # Thirty videos worth of data
  no_sequences = 30

  # Videos are going to be 30 frames in length
  sequence_length = 30
  
  for sign in signs: 
    for sequence in range(no_sequences):
      try: 
        os.makedirs(os.path.join(DATA_PATH, sign, str(sequence)))
      except:
        pass

if __name__ == '__main__':
  generate_data()
