import cv2 as cv
import mediapipe as mp


def main():
    cap = cv.VideoCapture(0)
    manos = mp.solutions.hands.Hands()
    dibujo = mp.solutions.drawing_utils
    estilos = mp.solutions.drawing_styles

    while True:
        exito, img = cap.read()
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        resultado = manos.process(imgRGB)

        land_marks = resultado.multi_hand_landmarks

        if land_marks:
            for land_mark in land_marks:
                dibujo.draw_land_marks(resultado,
                                       land_marks,
                                       manos.HAND_CONNECTIONS,
                                       estilos.get_default_hand_landmarks_style(),
                                       estilos.get_default_hand_connections_style())

        cv.imshow('video', img)
        cv.waitKey(1)


if __name__ == '__main__':
    main()
