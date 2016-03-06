from Tkinter import *

#---------------------------------
class IODirector(object):
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutDirector(IODirector):
    def write(self, msg):
        self.text_area.insert(END, msg)
        self.text_area.see(END)
    
    def flush(self):
        pass
