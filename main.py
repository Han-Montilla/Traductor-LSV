import cv2 as cv
import mediapipe as mp


def main():
    cap = cv.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

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

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
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
