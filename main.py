from turtle import color
from typing import Any
import cv2 as cv
from cv2 import blur
from cv2 import scaleAdd
from cv2 import adaptiveThreshold
from cv2 import CamShift
from matplotlib.pyplot import gray
import mediapipe as mp
from numpy import place


def main():
    # Leemos la camara
    cap = cv.VideoCapture(0)

    # Ajustamos los parametros para la deteccion

    # creamos un objeto que va a recibir la deteccion
    mp_hands = mp.solutions.hands

    # metodo que crea los puntos criticos calculados matematicamente en las manos
    mp_drawing = mp.solutions.drawing_utils

    # el estilo que tendran los puntos
    mp_drawing_styles = mp.solutions.drawing_styles

    # Verificamos si la camara funciona con las manos y agregamos parametros
    with mp_hands.Hands() as hands:
        while cap.isOpened():
            success, img = cap.read()
            h, w, c = img.shape

            if not success:
                print('ignoring')
                break

            img.flags.writeable = False
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            results = hands.process(img)

            img.flags.writeable = True
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

            # Si funciona aplicamos parametros para que se puedan ver en la camara
            if results.multi_hand_landmarks:

                # detecta los puntos en las manos y los dibuja
                for hand_landmarks in results.multi_hand_landmarks:
                    #definimos las variables de posicion del cuadro
                    x_max = 0
                    y_max = 0
                    x_min = w
                    y_min = h

                    #hacemos queel cuadro se adapte a las manos que salgan en la camara 

                    for lm in hand_landmarks.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)
                        if x > x_max:
                            x_max = x
                        if x < x_min:
                            x_min = x
                        if y > y_max:
                            y_max = y
                        if y < y_min:
                            y_min = y

                        #funcion el cual implementa el cuadro junto a la camara
                    cv.rectangle(img, (x_min-32, y_min-32),
                                 (x_max+32, y_max+32), (255, 0, 0), 5)
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            cv.imshow('video', img)
            cv.waitKey(5)


if __name__ == '__main__':
    main()
