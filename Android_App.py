
# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.widget import Widget
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture

# import cv2 as cv
# import numpy as np
# import mediapipe as mp
# import time

# Builder.load_string("""
# <StartScreen>:
#     BoxLayout:
#         Button:
#             markup: True
#             text: 'READY TO WORK WITH A HEALTHY NECK POSTURE?\\n\\n\\n[b]     TAP ANYWHERE ON THE SCREEN TO BEGIN![/b]'
#             font_size: '30sp'
#             on_press: root.manager.current = 'work'
#             background_normal: "images/img_bg.gif"
#             background_down: "images/img_bg2.gif"
#             canvas.before:
#                 Line:
#                     width: 3
#                     rectangle: (self.x, self.y, self.width, self.height)

        
# <WorkScreen>:
#     BoxLayout:
#         Button:
#             text: 'QUIT'
#             font_size: '30sp'
#             size_hint: 1, 0.1
#             on_press: root.manager.current = 'end'
#             background_normal: "images/img_bg.gif"
#             background_down: "images/img_bg2.gif"
        
              
# <EndScreen>:
#     BoxLayout:
#     Button:
#         text: 'This is how you fared:'
#         font_size: '30sp'
#         on_press: root.manager.current = 'start'
#         background_normal: "images/img_bg.gif"
#         background_down: "images/img_bg2.gif"
# """)

# # Declare both screens
# class StartScreen(Screen):
#     pass

# class WorkScreen(Screen):
#     pass

# class EndScreen(Screen):
#     pass

# class TestApp(App):

#     def build(self):
#         # Create the screen manager
#         sm = ScreenManager()
#         sm.add_widget(StartScreen(name='start'))
#         sm.add_widget(WorkScreen(name='work'))
#         sm.add_widget(EndScreen(name='end'))
#         return sm
    

# if __name__ == '__main__':
#     TestApp().run()
#     cv.destroyAllWindows()