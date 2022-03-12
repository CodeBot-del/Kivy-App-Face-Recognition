import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        # number of columns
        self.cols = 2  
        # Layouts imported comes with different components such as widgets and stuff.
        self.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False)
        self.add_widget(self.name)
        
        self.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.add_widget(self.lastName)

        self.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.add_widget(self.email)
        
        self.submitBtn = Button(text="Submit", fontsize=40)
        self.add_widget(self.submitBtn)


class MyApp(App):
    def build(self):
        return MyGrid()
    
if __name__ == '__main__':
    MyApp().run()
    