from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.image import Image
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    
    # def build(self):
    #     layout = FloatLayout()
    #     self.image = Image(
    #         size_hint= (0.3,0.3),
    #         pos_hint= {"x": 0.03, "top": 1}
    #     )
    #     layout.add_widget(self.image)
    #     # layout.add_widget(RaisedButton(
    #     #     text="CLICK HERE",
    #     #     pos_hint={'center_x': .5, 'center_y': .5}, 
    #     #     size_hint=(None, None)
    #     # ))
    #     self.capture = cv2.imread('cena.jpeg')
    #     Clock.schedule_interval(self.load_image, 1.0/30.0)
    #     return layout
    
    # def load_image(self, *args):
    #     frame = self.capture
    #     #Frame initialize
    #     self.image_frame = frame
    #     buffer = cv2.flip(frame, 0).tostring()
    #     texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    #     texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
    #     self.image.texture = texture
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")


class MyMainApp (App):
    def build(self):
        
        return kv
    

        
    
    
if __name__ == "__main__":
    MyMainApp().run()
    
    