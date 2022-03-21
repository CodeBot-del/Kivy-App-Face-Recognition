from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
import cv2  
from kivymd.uix.label import MDLabel
import numpy as np

class MainApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image(source="cena.jpeg")
        self.label = MDLabel()
        layout.add_widget(self.image)
        layout.add_widget(self.label)
        self.save_img_button = MDRaisedButton(
            text="CLICK HERE",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None)
        )
        self.save_img_button.bind(on_press=self.take_picture)
        layout.add_widget(self.save_img_button)
        return layout
    
    def take_picture(self, *args):
        pass 
    
    
if __name__ == '__main__':
    MainApp().run()