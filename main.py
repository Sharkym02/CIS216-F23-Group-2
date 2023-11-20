#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, TclError, filedialog, font
#from tkinter.scrolledtext import ScrolledText as Text
#from tkinter.colorchooser import askcolor

class GameCanvas(Canvas):
	def __init__(self, root, *args, **kwargs):
		# https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html
		Canvas.__init__(self, root, *args, **kwargs)
		# self._root = root
		self.configure(bg="green")

		self.create_text(20, 30, anchor=W, font="Ubuntu",
            text="This is canvas drawing")
		
		return

class MenuBar(Menu):
	def __init__(self, root, *args, **kwargs):
		Menu.__init__(self, root, *args, **kwargs)
		# self._root = root
		gameMenu = Menu(self, tearoff=0)

		gameMenu.add_command(label="New Game")
		# Additional buttons could be: Undo, Redo (?), Scores

		self.add_cascade(label="Game", menu = gameMenu)

		root.config(menu=self)
		return


if __name__ == "__main__":
	root = Tk()
	#frame = ttk.Frame(root,padding=10)

	canvas = GameCanvas(root)
	menuBar = MenuBar(root)
	canvas.pack(expand=True, fill="both")
	
	root.geometry("640x480")
	root.mainloop()
