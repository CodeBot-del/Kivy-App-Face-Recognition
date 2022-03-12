from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image
# from kivy.uix.widget import Widget

from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
import cv2 
import numpy as np
import face_recognition
import os



class SayHello(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        #put some margins around the window
        self.window.size_hint = (0.6, 0.7)
        #put it to the center
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        #add widgets to window
        
        #Label widget 
        self.welcome = Label(
            text="ALPHA AI",
            font_size = 50,
            bold = True,
            color='#212529'
            )
        
        self.window.add_widget(self.welcome)
        
        #image widget 
        self.stream = Image(
            # source="loader.gif", 
            # size_hint=(10,5), 
            # allow_stretch=True
            
            )
        self.window.add_widget(self.stream)
        
        #Label widget 
        self.greeting = Label(
            text="Welcome to Alpha AI",
            font_size = 18,
            color='#8d99ae'
            )
        
        self.window.add_widget(self.greeting)
        #text input widget 
        self.user = TextInput(
            multiline=False,
            padding_y = (20,20),
            size_hint = (1, 0.5)
            )
        
        # self.window.add_widget(self.user)
        #button widget 
        self.button = Button(
            text="FACIAL SCAN",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#184e77',
            color='#168aad'
            )
        
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
        
        
        
        self.button1 = Button(
            text="QR & BARCODE SCAN",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#184e77',
            color='#168aad',
            
            )
        
        self.button1.bind(on_press=self.callback2)
        self.window.add_widget(self.button1)
        
        self.button2 = Button(
            text="OPTIONS",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#184e77',
            color='#168aad'
            )
        
        self.button2.bind(on_press=self.callback)
        self.window.add_widget(self.button2)
        
        self.button3 = Button(
            text="HELP",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#184e77',
            color='#168aad'
            )
        
        self.button3.bind(on_press=self.popup)
        self.window.add_widget(self.button3)
        
        return self.window
        
    def callback(self, instance):
        
        path = 'imagesRecognition'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)

        #import the images from the directory
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
            
        print(classNames)

        #function to encode all images in the directory
        def findEncodings(images):
            encodeList = [] 
            for img in images:
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        encodeListKnown = findEncodings(images)
        print('################------ Encoding Complete ------################')

        #get the image to match with... For now we read an image, later on we will read from webcam (cv2.VideoCapture())

        cap = cv2.imread('chan.jpg')

        while True:
            # success, img = cap.read() #this line to be used when reading from webcam
            img = cap
            imgS = cv2.resize(img,(0,0),None,0.25,0.25) #compress the image to improve performance
            imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            
            facesCurFrame = face_recognition.face_locations(imgS) #find location of all faces in the image
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame) #find encodings of all the faces in the image
            
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame): #this grabs both the encodings and the locations of the faces in the current frame
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  #compare the image encodings with the known encodings
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  #Find how much the faces differ between the image and the known
                # print(faceDis)
                matchIndex = np.argmin(faceDis)  #take the lowest face distance to be the match 
                if matchIndex < 0.5:    # accept match index lower than 0.5... for the sake of accuracy
                    matchIndex = matchIndex
                
                
                if matches[matchIndex]:
                    
                    name = classNames[matchIndex].upper()  #Get the Name of the image(person) that matched successfully
                    # print(name)
                    y1,x1,y2,x2 = faceLoc
                    # y1,x1,y2,x2 = y1*4,x1*4,y2*4,x2*4 
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img, (x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED) #starting point on height reduced by -35 to be a little lower so we can write the name on top of this rectangle
                    cv2.putText(img,name, (x2, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    
                else:
                    name = "unknown"
                    y1,x1,y2,x2 = faceLoc
                    # y1,x1,y2,x2 = y1*4,x1*4,y2*4,x2*4 
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img, (x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED) #starting point on height reduced by -35 to be a little lower so we can write the name on top of this rectangle
                    cv2.putText(img,name, (x2, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    
                    
            ###################################  INTO THE BADLANDS  #################################################################################
            # img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)  #reduce size by scale 
            # img = cv2.resize(img, (900,600))
            
            
            # cv2.imwrite('result.jpg', img)
            # self.stream = cv2.imread('result.jpg')
            # frame = self.stream
            # self.image_frame = frame
            # buffer = cv2.flip(frame, 0).tostring()
            # texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            # texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            # self.stream.texture = texture
            
            
        
        # self.stream.source = "http://loyalkng.com/wp-content/uploads/2009/12/hps-computer-webcams-a"
            # self.stream = cv2.imshow('Results',img)
            
            self.capture = img
            Clock.schedule_interval(self.load_image, 1.0/30.0)
                
    def load_image(self, *args):
        frame = self.capture
        #Frame initialize
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.stream.texture = texture
            
        # cv2.imshow('Results',img)
        # cv2.waitKey(0)
            ################################################################################################################################
            
    def callback2(self, instance):
        self.stream.source = "https://cdn3.vectorstock.com/i/1000x1000/18/12/qr-and-barcode-mixwd-scanning-scan-me-concept-vector-29001812.jpg"
         
    def popup(self, instance):
        popup = Popup(
            title='Help Manual', 
            content = Label(
                text='Fake ID scanner is a product of Alpha AI \n It enables you to detect a Fake ID card. \n Easily scan an ID with your camera \n to detect if it belongs to your \n organization or it is fraudulent. \n \n Relax! \n 1. To scan faces from ID cards, \n press the FACIAL SCAN button. \n 2. To scan QR codes and Barcodes \n press QR & BARCODE SCAN button. \n 3. To change some scan options \n press the OPTIONS button.',
                color='#8d99ae'
                ),
            size_hint = (None,.5),
            width=(300)
            
            
            
        )
        popup.open()
        

        

if __name__ == "__main__":
    SayHello().run()
