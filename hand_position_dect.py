import cv2
# import numpy as np
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
frame_width, frame_height = 640, 480
click_active = False
mouse_down = False
numberOfClickes = 0
p_x, p_y = pyautogui.position()


def finger_isUp(arg_list):

    indexs = [8, 12, 16, 20]
    fingers_list = []
    # thumb
    if arg_list[4][0] > arg_list[3][0]:
        fingers_list.append(1)
    else:
        fingers_list.append(0)
    # fingers
    for x in indexs:
        if arg_list[x][1] < arg_list[x-2][1]:
            fingers_list.append(1)
        else:
            fingers_list.append(0)

    return fingers_list


def function(arg_hand):

    cord_list = []
    normailzed_list = []

    for cord in arg_hand.landmark:

        # cx, cy = round(cord.x, 3), round(cord.y, 3)
        cx, cy = cord.x, cord.y

        cord_list.append([cx, cy])

    return cord_list


mp_drawings = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
record_video = cv2.VideoWriter("Cam.mp4", fourcc, 20.0, (frame_width, frame_height))


with mp_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=.05) as hands:

    while cap.isOpened():

        ret, frame = cap.read()
    # convert BGR to RGB and fliping image on y axis
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False  # improve performance

        result = hands.process(image)

        image.flags.writeable = True
    # convert RGB to BGR :
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # print(result.multi_handedness)

        if result.multi_hand_landmarks:

            for num, hand in enumerate(result.multi_hand_landmarks):
                mp_drawings.draw_landmarks(image, hand, mp_hand.HAND_CONNECTIONS,
                                           mp_drawings.DrawingSpec(color=(0, 0, 255),
                                                                   thickness=2, circle_radius=3))
                coordinates = function(hand)
                finnger_list = finger_isUp(coordinates)

                p_x, p_y = pyautogui.position()
                # Left Click :
                # if finnger_list[1] and finnger_list[0]:
                #
                #     if click_active:
                #
                #         print("true")
                #         pyautogui.click(p_x, p_y)
                #         numberOfClickes += 1
                #         click_active = False
                #  print("done")
                # Right Click :
            #     if finnger_list[1] and finnger_list[4]:
            #         # print("Right click")
            #
            #         if click_active:
            #
            #             pyautogui.click(button='right')
            #             click_active = False
            #
            #     if not finnger_list[0] and not finnger_list[4]:
            #
            #         click_active = True
            # # Scroll :
            #     if finnger_list[1] and finnger_list[2]:
            #         mouse_y = (coordinates[8][1] * frame_height - 80)/220*screen_h
            #         scroll = int(p_y - mouse_y)
            #         print(scroll)
            #         pyautogui.scroll(scroll)
            #         p_y = mouse_y
            #         # print("up")

            # Mouse Movement
                if finnger_list[1]:

                    if finnger_list[0]:
                        print("Thumb UP")
                        if click_active:
                            pyautogui.click(p_x, p_y)
                            numberOfClickes += 1
                            click_active = False

                    elif finnger_list[4]:
                        print("Little finger UP")

                        if click_active:
                            pyautogui.click(button='right')
                            click_active = False

                    elif finnger_list[2] and not finnger_list[0] and not finnger_list[3]:

                        mouse_y = (coordinates[8][1] * frame_height - 80) / 220 * screen_h
                        scroll = int(p_y - mouse_y)
                        print(scroll)
                        pyautogui.scroll(scroll)
                        p_y = mouse_y

                    else:

                        click_active = True
                        raw_x, raw_y = coordinates[8][0], coordinates[8][1]

                        mouse_x, mouse_y = (raw_x * frame_width - 100)/440*screen_w,\
                                           (raw_y * frame_height - 80)/220*screen_h
                        # Smooth Movementq

                        mouse_x = p_x + (mouse_x - p_x) / 2
                        mouse_y = p_y + (mouse_y - p_y) / 2

                        # Coordinate Constrains
                        if mouse_x >= screen_w:
                            mouse_x = screen_w - 5
                        if mouse_x <= 0:
                            mouse_x = 0 + 5

                        if mouse_y >= screen_h - 5:
                            mouse_y = screen_h - 5
                        if mouse_y <= 0:
                            mouse_y = 0 + 5

                        if finnger_list[2] and finnger_list[3]:
                            if not mouse_down:
                                mouse_down = True
                                pyautogui.mouseDown()
                            # pyautogui.moveTo(mouse_x, mouse_y, duration=0.1, tween=pyautogui.easeInOutQuad)
                        else:
                            if mouse_down:
                                pyautogui.mouseUp()
                                mouse_down = False

                        # print(mouse_down)
                        pyautogui.moveTo(mouse_x, mouse_y, duration=0.1, tween=pyautogui.easeInOutQuad)
                        p_x, p_y = mouse_x, mouse_y
                else:
                    if mouse_down:
                        pyautogui.mouseUp()
                        mouse_down = False
        cv2.rectangle(image, (100, 80), (540, 300), (255, 0, 0), 3)
        record_video.write(image)
        cv2.imshow("video", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("True")

            break

cv2.destroyAllWindows()
cap.release()
print(numberOfClickes)
