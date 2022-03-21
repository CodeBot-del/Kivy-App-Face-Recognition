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
        self.image = Image(source="sphere.jpg")
        self.label = MDLabel()
        layout.add_widget(self.image)
        layout.add_widget(self.label)
        self.save_img_button = MDRaisedButton(
            text="Remove BG",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None)
        )
        self.save_img_button.bind(on_press=self.take_picture)
        layout.add_widget(self.save_img_button)
        return layout
    
    def take_picture(self, *args):
        #read the image
        image = cv2.imread(self.image.source)
        #create a mask/ a black image that will separate the foreground from background of original image
        mask = np.zeros(image.shape[:2], np.uint8)
        backgroundModel = np.zeros((1,65), np.float64)
        foregroundModel = np.zeros((1,65), np.float64)
        
        #mark the image    
        rectangle = (0,0, int(self.image.texture_size[1]), int(self.image.texture_size[0]))
        # rectangle = (0,0, 16, 16)
        
        #parameters passed to the grabcut method
        # values = (
        #     ("Definite Background", cv2.GC_BGD),
        #     ("Probable Background", cv2.GC_PR_BGD),
        #     ("Definite Foreground", cv2.GC_FGD),
        #     ("Probable Foreground", cv2.GC_PR_FGD),
        # )
        
        #crop the foreground 
        cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 4, cv2.GC_INIT_WITH_RECT)
        
        #the resulting removed background image
        finalmask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1).astype('uint8')    
        
        image = image * finalmask[:,:, np.newaxis]
        
        #convert it to transparent
        
        b, g, r = cv2.split(image)
        gray_layer = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(gray_layer, 0, 255, cv2.THRESH_BINARY)
        
        rgba = [b, g, r, alpha]
        destination = cv2.merge(rgba, 4)
        cv2.imwrite("results2.png", destination)
        self.label.text = "Removed Background successfully"

    
    
if __name__ == '__main__':
    MainApp().run()