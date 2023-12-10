#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, TclError, filedialog, font
#from tkinter.scrolledtext import ScrolledText as Text
#from tkinter.colorchooser import askcolor
from gamelogic import Card, SpiderGame, PyTkImagePool
from vector2 import Vector2
from functools import partial 
#from PIL import Image, ImageTk

#TODO: We should make this adjustable in real time -BM
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
#This should be a set/get if it's going to change -BM
SCREEN_CENTER_X = SCREEN_WIDTH/2
SCREEN_CENTER_Y = SCREEN_HEIGHT/2

CARD_SIZE = Vector2(42,60)

class GameCanvas(Canvas):
	def __init__(self, root, spider:SpiderGame, *args, **kwargs):

		self.spider = spider
		self.pool = PyTkImagePool()
		self.mousePosition = Vector2()
		self.selectedCard = Vector2(-1, -1)

		# https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html
		Canvas.__init__(self, root, *args, **kwargs)

		#self.bind("<1>", lambda x: self.handle_click(x))
		#No need for this, probably
		#self.bind("<Motion>", lambda x: self.handle_mouseover(x))
		# self._root = root
		self.redraw_canvas()

		
		return
	
	def handle_click(self,event):
		print(event.widget)
		print(event.x, event.y)
		self.mousePosition = Vector2(event.x, event.y)
		self.redraw_canvas()

	def handle_card_click(self, event, card_col:int, card_row:int, card:Card):
		#print(card_col, card_row)
		print("Clicked card "+str(card))
		self.mousePosition=Vector2(event.x,event.y)

		

		if card.faceUp:
			if self.selectedCard.IsPositive(): #If already has selection
				#Interact with gamelogic here and attempt to move card(s) to another
				#column
				spider.tryMoveCards(self.selectedCard.x, self.selectedCard.y, card_col, card_row)

				self.selectedCard = Vector2(-1,-1) # Removes the previous card's
				# selection and returns it to "default"
				pass
			else: #new selection
				numValidDescending = spider.numValidDescending(card_col,card_row)
				if numValidDescending > 0:
					self.selectedCard = Vector2(card_col,card_row)
				print("Got a descending column of "+str(numValidDescending)+" cards")
		#print(event.x, event.y)
		self.redraw_canvas()

	def handle_column_click(self, event, card_col:int):
		if self.selectedCard.IsPositive():
			print("clicked a column with a selection...")
			if self.spider.tryMoveCards(self.selectedCard.x, self.selectedCard.y, card_col, 0):
				self.selectedCard = Vector2(-1,-1)
				self.redraw_canvas()

				if self.spider.isGameWon():
					#TODO: pop-up here
					pass
	
	def handle_stock_click(self, event):
		self.spider.drawFromStock()
		self.redraw_canvas()

	def handle_mouseover(self,event):
		self.mousePosition=Vector2(event.x, event.y)
		self.redraw_canvas()

	def redraw_canvas(self):
		self.delete("all") #Clear canvas
		self.configure(bg="green")

		# self.create_text(20,SCREEN_HEIGHT-20, anchor=W, font="Ubuntu",
		# 	text=str(self.mousePosition))

		
		for colNum in range(self.spider.NUM_COLUMNS):
			col = self.spider.columns[colNum]
			
			#This is a clickable column so you can drag cards into it. YES THERE NEEDS TO BE FILL YOU CAN'T LEAVE IT TRANSPARENT
			invisible_column = self.create_rectangle(30+colNum*50, 20, 30+colNum*50+CARD_SIZE.x, 200, outline="green", fill="green", width=2)
			self.tag_bind(invisible_column, "<1>", lambda e, x=colNum: self.handle_column_click(e,x))

			for i in range(len(col)):
				#card = col[i]
				image = self.pool.get_image(col[i])

				#args are xPos, yPos, image, anchor
				img_obj = self.create_image(50+colNum*50,50+i*16,image=image,anchor=CENTER)

				#DEBUG DRAW
				#self.create_rectangle(50+colNum*50,50+i*16, 50+colNum*50+64,50+i*16+64, outline="orange", fill="", width=2)

				#Due to how lambdas work you have to force assigning to a new variable using = sign and then
				#refer to those variables within the lambda expression. Otherwise without the bind
				#it will just refer to the final created lambda in the for loop no matter what you
				#click on -BM
				# (e does not need to be bound here since it's just the click event)
				self.tag_bind(img_obj,"<1>",lambda e,x=colNum,y=i,card=col[i]: self.handle_card_click(e,x,y,card))
		
		self.create_text(SCREEN_WIDTH-10, SCREEN_HEIGHT-70-40, anchor=E, font="Ubuntu",
            text="Click to draw more cards")
		self.create_text(10, SCREEN_HEIGHT-70-40, anchor=W, font="Ubuntu",
            text="Completed cards go here")
		
		# if spider.debug_mode:
		# 	self.create_text(10, SCREEN_HEIGHT-200, anchor=W, font="Ubuntu",
        #     text="DEBUG MODE")

		for drawNum in range(len(self.spider.deck)//10): #No, this isn't a typo, it's the floor division operator.
			image = self.pool.get_facedown_image()
			img_obj = self.create_image(SCREEN_WIDTH-50-10*drawNum,SCREEN_HEIGHT-70,image=image,anchor=CENTER)
			self.tag_bind(img_obj, "<1>", self.handle_stock_click)

		for drawNum in range(self.spider.completedColumns):
			image = self.pool.get_image(Card(1,0,True))
			img_obj = self.create_image(25+(CARD_SIZE.x+4)*drawNum,SCREEN_HEIGHT-70,image=image,anchor=CENTER)

		if (self.selectedCard.IsPositive()): # TODO: Make the highlight around the card.
			#For some insane reason create_rectangle is x1,y1, x2,y2 instead of x,y,w,h
			src = Vector2(self.selectedCard.x*50+29, self.selectedCard.y*16+20)
			
			rect_height = src.y+CARD_SIZE.y+16*(spider.numValidDescending(self.selectedCard.x, self.selectedCard.y)-1)

			self.create_rectangle(src.x, src.y, src.x+CARD_SIZE.x, rect_height, outline="orange", fill="", width=2)

class MenuBar(Menu):
	def __init__(self, root, spider, *args, **kwargs):
		Menu.__init__(self, root, *args, **kwargs)
		self.spider = spider
		# self._root = root
		gameMenu = Menu(self, tearoff=0)

		gameMenu.add_command(label="New Game")
		# Additional buttons could be: Undo, Redo (?), Scores

		self.add_cascade(label="Game", menu = gameMenu)

		debugOptions = Menu(self,tearoff=0)
		#If not assigned to self it will get garbage collected even though add_checkbutton should store the ref... oh well -BM
		self.tkVar = BooleanVar(name="DebugMode")
		self.tkVar.trace_add("write",callback=self.set_debug_mode )
		debugOptions.add_checkbutton(label="Allow dragging and dropping onto any card", variable=self.tkVar, onvalue=True, offvalue=False)


		#debugOptions.add_checkbutton(label="Free space column", variable=self.tkVar, onvalue=True, offvalue=False)

		self.add_cascade(label="Difficulty Options", menu=debugOptions)

		self.add_cascade(label="How To Play")

		root.config(menu=self)
		return
	
	def set_debug_mode(self,var_name,idx,access_mode):
		print(self.tkVar.get())
		self.spider.debug_mode = self.tkVar.get()


if __name__ == "__main__":


	root = Tk()
	spider = SpiderGame()
	#frame = ttk.Frame(root,padding=10)

	canvas = GameCanvas(root, spider)
	menuBar = MenuBar(root,spider)
	canvas.pack(expand=True, fill="both")
	
	root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
	root.resizable(False, False)
	root.mainloop()
