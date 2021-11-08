# Program to Show how to use images in kivy

# import kivy module
import kivy
	
# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# The Image widget is used to display an image
# this module contain all features of images
from kivy.uix.image import Image

# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget

# to change the kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)


# creating the App class
class MyApp(App):

	# defining build()
	
	def build(self):
		
		# loading image
		self.img = Image(source ='images/img_bg.gif')

		# By default, the image is centered and fits
		# inside the widget bounding box.
		# If you don’t want that,
		# you can set allow_stretch to
		# True and keep_ratio to False.
		self.img.allow_stretch = True
		self.img.keep_ratio = True

		# Providing Size to the image
		# it varies from 0 to 1
		#self.img.size_hint_x = 1
		#self.img.size_hint_y = 1

		# Position set
		self.img.pos = (200, 200)

		# Opacity adjust the fadeness of the image if
		# 0 then it is complete black
		# 1 then original
		# it varies from 0 to 1
		self.img.opacity = 1
		

		# adding image to widget
		s = Widget()
		s.add_widget(self.img)

		# return widget
		return s

# run the app
MyApp().run()
