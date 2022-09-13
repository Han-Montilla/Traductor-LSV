import cv2
import numpy as np
import mediapipe as mp
import os

# Global Variables
mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
signs = np.array(['a']) # detectable signs


# utilidad
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

def main():
  cap = cv2.VideoCapture(0)
  # Set mediapipe model 
  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
      # Read feed
      ret, frame = cap.read()

      # Make detections
      image, results = mediapipe_detection(frame, holistic)
      
      # Draw landmarks
      draw_styled_landmarks(mp_drawing, mp_holistic, image, results)

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
  
  cap = cv2.VideoCapture(0)
  # Set mediapipe model 
  with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    # Loop through actions
    for sign in signs:
      # Loop through sequences aka videos
      for sequence in range(no_sequences):
        # Loop through video length aka sequence length
        for frame_num in range(sequence_length):
          # Read feed
          ret, frame = cap.read()

          # Make detections
          image, results = mediapipe_detection(frame, holistic)

          # Draw landmarks
          draw_styled_landmarks(image, results)
          
          # NEW Apply wait logic
          if frame_num == 0: 
            cv2.putText(image, 'STARTING COLLECTION', (120,200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
            cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(sign, sequence), (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            # Show to screen
            cv2.imshow('OpenCV Feed', image)
            cv2.waitKey(2000)
          else: 
            cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(sign, sequence), (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            # Show to screen
            cv2.imshow('OpenCV Feed', image)
          
          # NEW Export keypoints
          keypoints = extract_keypoints(results)
          npy_path = os.path.join(DATA_PATH, sign, str(sequence), str(frame_num))
          np.save(npy_path, keypoints)

          # Break gracefully
          if cv2.waitKey(10) & 0xFF == ord('q'):
              break
            
    cap.release()
    cv2.destroyAllWindows()


# Preprocess Data and Create Labels and Features
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.utils import to_categorical

def process_signs():
  label_map = { label: num for num, label in enumerate(signs) }

if __name__ == '__main__':
  generate_data()
