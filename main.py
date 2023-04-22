import tkinter

from bracelet import Bracelet
from gui import GUI
bracelet = Bracelet()
root = tkinter.Tk()
gui = GUI(root)
gui.run()
