import cv2 as cv
import mediapipe as mp


def main():
    cap = cv.VideoCapture(0)
    manos = mp.solutions.hands.Hands()
    dibujo = mp.solutions.drawing_utils

    while True:
        exito, img = cap.read()
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        res = manos.process(imgRGB)

        cv.imshow('video', img)
        cv.waitKey(1)


if __name__ == '__main__':
    main()
