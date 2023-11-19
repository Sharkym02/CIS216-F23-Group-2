#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, TclError, filedialog, font
#from tkinter.scrolledtext import ScrolledText as Text
#from tkinter.colorchooser import askcolor

if __name__ == "__main__":
	root = Tk()
	#frame = ttk.Frame(root,padding=10)
	
	#https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html
	canvas = Canvas(root, bg="green", height=480, width=640)
	canvas.create_text(20, 30, anchor=W, font="Ubuntu",
            text="This is canvas drawing")
	canvas.pack()
	
	root.geometry("640x480")
	root.mainloop()
