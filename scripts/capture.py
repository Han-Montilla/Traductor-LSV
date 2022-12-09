import cv2 
from uuid import uuid1
from time import sleep
from definitions import SINGS, CAPTURED_IMAGES_DIR
from os.path import join

SNAPSHOTS = 10
WAIT_PER_SIGN = 5
WAIT_PER_SNAPSHOT = 2

cap = cv2.VideoCapture(0)

for sign in SINGS:
  print(f'Capturing sign {sign} in {WAIT_PER_SIGN}s')
  sleep(WAIT_PER_SIGN)

  for i in range(SNAPSHOTS):
    print(f'Collecting image {i + 1} for sign {sign} in {WAIT_PER_SNAPSHOT}')
    sleep(WAIT_PER_SNAPSHOT)
    
    ret, frame = cap.read()
    img_path = join(CAPTURED_IMAGES_DIR, f'{sign}.{uuid1()}.jpg')
    cv2.imwrite(img_path, frame)
    cv2.imshow('frame', frame)
    
cap.release()
cv2.destroyAllWindows()