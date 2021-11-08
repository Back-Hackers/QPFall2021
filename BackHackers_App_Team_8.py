# Imports
import threading
from functools import partial
import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# defining global variables that determine neck posture
midline = 140
interval = 30
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
pose_coord = [[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]
pose_coord = np.array(pose_coord)

class MainScreen(Screen):
    pass


class Manager(ScreenManager):
    pass


Builder.load_string('''
<MainScreen>:
    name: "Test"

    FloatLayout:
        Label:
            text: "Webcam from OpenCV?"
            pos_hint: {"x":0.0, "y":0.8}
            size_hint: 1.0, 0.2

        Image:
            # this is where the video will show
            # the id allows easy access
            id: vid
            size_hint: 1, 0.6
            allow_stretch: True  # allow the video image to be scaled
            keep_ratio: True  # keep the aspect ratio so people don't look squashed
            pos_hint: {'center_x':0.5, 'top':0.8}

        Button:
            text: 'Stop Video'
            pos_hint: {"x":0.0, "y":0.0}
            size_hint: 1.0, 0.2
            font_size: 50
            on_release: app.stop_vid()
''')


class Main(App):
    def build(self):

        # start the camera access code on a separate thread
        # if this was done on the main thread, GUI would stop
        # daemon=True means kill this thread when app stops
        threading.Thread(target=self.doit, daemon=True).start()

        sm = ScreenManager()
        self.main_screen = MainScreen()
        sm.add_widget(self.main_screen)
        return sm

    def doit(self):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop

        # make a window for use by cv2
        # flags allow resizing without regard to aspect ratio
        cv.namedWindow('Hidden', cv.WINDOW_NORMAL | cv.WINDOW_FREERATIO)

        # resize the window to (0,0) to make it invisible
        cv.resizeWindow('Hidden', 0, 0)
        cam = cv.VideoCapture(0)
        if not cam.isOpened():
                raise IOError("Cannot open webcam")

        y_dist_left = 0
        y_dist_avg = 0
        y_dist_array = []

        # start processing loop
        while (self.do_vid):
            ret, frame = cam.read()
            frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_AREA)
            results = pose.process(frame)

            frame = cv.rectangle(frame,(40,40),(210,110),(0,0,0),thickness=cv.FILLED)
            frame = cv.rectangle(frame,(50,50),(200,100),(200,145,59),thickness=cv.FILLED)
            frame = cv.putText(frame, 'Neck:', (70,90), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            
            if results.pose_landmarks is not None:    
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w,c = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    pose_coord[id] = [cx,cy]

                y_dist_left = pose_coord[11][1] - pose_coord[9][1]    
                if y_dist_left > (midline + interval):
                    frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
                    frame = cv.rectangle(frame,(50,130),(200,340),(230,124,176),thickness=cv.FILLED)
                    frame = cv.putText(frame, 'Bend', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
                    frame = cv.putText(frame, 'a bit', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
                    frame = cv.putText(frame, 'forward!', (60,290), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)

                elif y_dist_left < (midline - interval):
                    frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
                    frame = cv.rectangle(frame,(50,130),(200,340),(160,210,196),thickness=cv.FILLED)
                    frame = cv.putText(frame, 'Bend', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
                    frame = cv.putText(frame, 'a bit', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
                    frame = cv.putText(frame, 'back!', (60,290), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)

                else:
                    frame = cv.rectangle(frame,(40,120),(210,350),(0,0,0),thickness=cv.FILLED)
                    frame = cv.rectangle(frame,(50,130),(200,340),(130,140,245),thickness=cv.FILLED)
                    frame = cv.putText(frame, 'You\'re', (70,190), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
                    frame = cv.putText(frame, 'Good!', (70,240), cv.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv.LINE_AA)
            
            # send this frame to the kivy Image Widget
            # Must use Clock.schedule_once to get this bit of code
            # to run back on the main thread (required for GUI operations)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            cv.imshow('Hidden', frame)
            cv.waitKey(1)
        cam.release()
        cv.destroyAllWindows()

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False

    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.main_screen.ids.vid.texture = texture


if __name__ == '__main__':
    Main().run()