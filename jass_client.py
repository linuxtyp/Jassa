import socket
import threading

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField


KV = '''
Screen:
	MDLabel:
	    id: Karten
	    text: ""
	    pos_hint: {"center_x": .6, "center_y": .6}
	MDTextField:
	    id: card
	    mode: "rectangle"
	    hint_text: "Input the index"
	    helper_text: "Index is the number next to the card"
	    helper_text_mode: "on_focus"
	    pos_hint: {"center_x": .5, "bottom_y": .0}
	MDIconButton:
	    icon:"check"
	    pos_hint: {"center_x": .9, "bottom_y": .0}
	    on_release: app.send()

	MDFillRoundFlatButton:
	    text: "Connect"
	    pos_hint: {"center_x": .5, "center_y": .8}
	    font_size: 15
	    on_release: app.connect()
	MDFillRoundFlatButton:
	    text: "Disconnect"
	    pos_hint: {"center_x": .5, "center_y": .2}
	    font_size: 15
	    on_release: app.disconnect()
'''
from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton


class MainApp(MDApp):
	dialog=None
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Indigo"
		self.theme_cls.accent_palette = "Blue"
		return Builder.load_string(KV)
	def send(self):
		global wait
		#wait = 0
		print("send")
		re = int(self.root.ids.card.text)
		print("message:",re)
		s.send(bytes(str(re),"utf-8"))

		unenc = s.recv(1024)
		msg = (unenc.decode("utf-8"))
		self.root.ids.Karten.text = msg
		print("Received")
	def connect(self):
		global s
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((socket.gethostname(),1234))
		x = 0
		while x == 0:
			unenc = s.recv(1024)
			msg = (unenc.decode("utf-8"))
			self.root.ids.Karten.text = msg
			print("Received")
			x = 1
	def disconnect(self):
		s.stop(clientsocket)
MainApp().run()





