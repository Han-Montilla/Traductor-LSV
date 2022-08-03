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
    #Leemos la camara
    cap = cv.VideoCapture(0)

    #Ajustamos los parametros para la deteccion

    #creamos un objeto que va a recibir la deteccion
    mp_hands = mp.solutions.hands

    #metodo que crea los puntos criticos calculados matematicamente en las manos
    mp_drawing = mp.solutions.drawing_utils

    #el estilo que tendran los puntos
    mp_drawing_styles = mp.solutions.drawing_styles

    #Verificamos si la camara funciona con las manos y agregamos parametros  
    with mp_hands.Hands() as hands:
        while cap.isOpened():
            success, img = cap.read()
            if not success:
                print('ignoring')
                break

            img.flags.writeable = False
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            results = hands.process(img)

            img.flags.writeable = True
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            


            #Si funciona aplicamos parametros para que se puedan ver en la camara
            if results.multi_hand_landmarks:               
                
                #detecta los puntos en las manos y los dibuja
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            

            cv.rectangle(img,(100-2,300-2),(100+3,300+3),(0,255,0),6)
            cv.imshow('video', img)
            cv.waitKey(5)


if __name__ == '__main__':
    main()
