from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from scrapper import exec

Window.size = (400, 400)

class UserGroup(Screen):
    allinonepc = ObjectProperty(None)
    laptopnotebook = ObjectProperty(None)
    desktopcomputers = ObjectProperty(None)
    mfm = ObjectProperty(None)
    server = ObjectProperty(None)
    speed = ObjectProperty(None)
    
    #test
    
    def insert_data(self):
        def chk_actives():
            actives=[]
            if self.allinonepc.active:
                actives.append('All in One PC')
            if self.laptopnotebook.active:
                actives.append('Laptop-Notebook')
            if self.desktopcomputers.active:
                actives.append('Desktop Computers')
            if self.mfm.active:
                actives.append('Multifunction Machines MFM')
            if self.server.active:
                actives.append('Server')
            return actives
        if chk_actives() == []:
            print('No Item selected')
        else:
            for i in chk_actives():
                exec(i, speed=eval(self.speed.text) if self.speed.text != '' else 2)


class Gemmy(App):

    def build(self):
        self.root = Builder.load_file('test.kv')
        return self.root


if __name__ == '__main__':
    Gemmy().run()
    

