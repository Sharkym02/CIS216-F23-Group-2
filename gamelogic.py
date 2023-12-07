import random
from enum import IntEnum
from typing import List, Dict
from tkinter import PhotoImage
from os import path

class TYPE(IntEnum):
	"""An IntEnum allows you to compare using the enum instead of the integer.
	Example: To check if a card is a spade, you can do card.value == TYPE.SPADE
	"""
	SPADE = 0
	HEART = 1
	CLUB = 2
	DIAMOND = 3

class Card:
	def __init__(self, value:int, suit:int, faceUp:bool):
		# spade: 0, heart: 1, club: 2, diamond: 3
		self.__value = value
		self.__suit = suit
		self.__faceUp = faceUp

	def __str__(self) -> str:
		"""Returns a string representation of the card. Useful for debugging.
		Example: str(card) returns "(2, HEART, up)" for a card that has a value
		of 2, is of the heart suit, and is currently facing up.
		"""
		s = f"({self.__value}, {TYPE(self.__suit).name}, "
		s+= self.__faceUp and "up" or "down"
		s+=")"
		return s
	
	@property
	def value(self):
		return self.__value
	
	@property
	def suit(self):
		return self.__suit
	
	@property
	def faceUp(self):
		return self.__faceUp
	
	@faceUp.setter
	def faceUp(self, faceUp:bool):
		self.__faceUp = faceUp

#Loads all images into memory
class PyTkImagePool():
	
	def __init__(self) -> None:
		self.d:Dict[int,PhotoImage] = {}
		for suit in [TYPE.SPADE, TYPE.HEART, TYPE.CLUB, TYPE.DIAMOND]:
			for card_num in range(1,14):
				val = suit.value*100 #0 -> 0, 1 -> 100, 2 -> 200
				val+=card_num #101, 102, etc

				file_name = path.join("Assets", suit.name.lower()+"s_"+str(card_num).zfill(2)+".png")

				self.d[val] = PhotoImage(file=file_name)
				
		self.d[0] = PhotoImage(file=path.join("Assets", "back.png"))

	def get_image(self, c: Card) -> PhotoImage:
		if (c.faceUp):
			return self.d[c.suit*100+c.value]
		return self.d[0]
	
	def get_facedown_image(self):
		return self.d[0]

class CardManager:
	# The end of the list is the top of the deck
	# The beginning of the list is the bottom of the deck
	def __init__(self, deck: list):
		self.deck = deck

	def createDeck(self):
    # make a deck with each card in it
		for x in range(1, 14):
			for y in range(4):
				self.deck[x+13*(y)] = Card(x, y, True)

	def reset(self):
		self.deck.clear()
		self.createDeck()

	def popTop(self):
		first = self.deck.pop(-1)
		return first

	def popBottom(self):
		last = self.deck.pop(0)
		return last

	def addTop(self, card: Card):
		self.deck.append(card)

	def addBottom(self, card: Card):
		self.deck.insert(0, card)

	def shuffle(self):
		random.shuffle(self.deck)

class Column(CardManager):
	def __init__(self, location, *args, **kwargs):
		Column.__init__(self, location, *args, **kwargs)


#Spider Solitiare
class SpiderGame():

	#Change this to 11 for debugging or some sort of easy mode with a free column
	NUM_COLUMNS = 10

	def __init__(self):

		self.deck:List[Card] = []
		"""The deck of cards. In spider solitiare, there are two decks totalling 104."""
		self.columns:List[List[Card]] = []
		"""All the columns of the play area. There are 10 in total."""
		self.completedColumns:int = 0
		"""When there are eight completed columns, there are no cards left on the board and the game is won."""

		#Spider uses two decks, so combine two decks
		self.deck+=SpiderGame.createDeck()
		self.deck+=SpiderGame.createDeck()

		#Wheee
		random.shuffle(self.deck)

		# Now lay out the columns. There will be 10 columns,
		# and the game starts with 4 columns containing 6 cards,
		# then 6 columns containing 5 cards.

		# TODO: this kind of code is horribly inefficient. In theory
		# all cards could be in one large array and objects are just
		# shuffled, then column begin/end is marked somewhere
		# (I will leave that to someone else to improve upon)

		#DON'T DO [[]]*10 IT WILL JUST COPY THE FIRST ARRAY REFERENCE TO THE OTHERS
		for i in range(SpiderGame.NUM_COLUMNS):
			self.columns.append([])


		#For four columns, move five cards into each column
		for col in range(4): #0,1,2,3
			for i in range(5):
				self.columns[col].append(self.deck.pop())

		#Repeat but now 4 cards
		for col in range(4,10): #4,5,6,7,8,9
			for i in range(4):
				self.columns[col].append(self.deck.pop())

		#Places faceup cards in all columns
		self.drawFromStock()

		print("Got "+str(self.getNumCardsOnField())+" cards on field, "+str(len(self.deck))+" cards remaining in draw pile")
		#for c in self.columns[0]:
		#	print(c)

	@staticmethod
	def createDeck() -> List[Card]:
    	# For spider solitiare, generate a deck of only 1 suit
		# Maybe we can generate more suits for harder difficulties later
		deck = []
		for x in range(1, 14):
			for y in range(4):
				deck.append(Card(x, TYPE.SPADE, False))
		assert len(deck)==52,"Size of deck is improper"
		return deck

	def getNumCardsOnField(self) -> int:
		total = 0
		for col in self.columns:
			total+=len(col)
		return total
	
	def tryMoveCards(self, srcColumn:int, srcRow:int, destColumn:int, destRow:int) -> bool:
		"""_summary_

		Args:
			srcColumn (int): _description_
			srcRow (int): _description_
			destColumn (int): _description_
			destRow (int): _description_

		Returns:
			bool: Returns true if this move is possible and the move succeeded.
		"""

		# Checks the moving card for being the bottom-most card and if its faced up.
		# The faced up check could probably be skipped as
		# ideally all of the faced up card should be at the top anyways.
		#if (srcRow + 1 != len(self.columns[srcColumn]) or not self.columns[srcColumn][srcRow].faceUp):
		#	return False



		# Short circuits the checks if destColumn has no cards and moves the card anyways.
		if (len(self.columns[destColumn]) <= 0):
			print("Trying to move to an empty column.")
			numToMove = self.numValidDescending(srcColumn,srcRow)
			print(f"Got {numToMove} cards to move.")
			# This is kind of tricky, we have to move the cards to the destination first
			# and THEN clear them from the source row. deleting an element from the array
			# will shift it down, so we should be able to just do it on the same row

			for i in range(numToMove):
				self.columns[destColumn].append(self.columns[srcColumn][srcRow])
				del self.columns[srcColumn][srcRow]
			self.revealCard(srcColumn)
			return True

		# Checks if dest column is face up... I can't tell what the first one is doing
		if (destRow + 1 != len(self.columns[destColumn]) or not self.columns[destColumn][destRow].faceUp):
			return False
		
		#if src is 1 less than dest, this is a valid move
		if (self.columns[srcColumn][srcRow].value == self.columns[destColumn][destRow].value - 1):
			
			#Refer to above comment -BM
			numToMove = self.numValidDescending(srcColumn,srcRow)
			for i in range(numToMove):
				self.columns[destColumn].append(self.columns[srcColumn][srcRow])
				del self.columns[srcColumn][srcRow]
			self.revealCard(srcColumn)
			self.checkAndMoveCompletedColumn(destColumn)
			return True

		return False
	
	def revealCard(self, column:int) -> bool:
		"""_summary_
			Reveals the bottommost card of the column.
		
		Returns:
			bool: Returns true if the upmost card was not revealed up and was revealed.
		"""
		if (len(self.columns[column]) <= 0):
			return False

		if (self.columns[column][len(self.columns[column]) - 1].faceUp):
			return False
		
		self.columns[column][len(self.columns[column]) - 1].faceUp = True
		return True
	
	def drawFromStock(self) -> bool:
		"""_summary_
			Draws from the stock pile and distributes the card to every column.
		
		Returns:
			bool: Returns true if any cards were distributed.
		"""
		maxDraw = min(10, len(self.deck))
		if (maxDraw < 1):
			return False
		
		for col in range(maxDraw):
			c = self.deck.pop()
			c.faceUp = True
			self.columns[col].append(c)

		return True
	
	# Checks if a column is descending, so you can select
	# a whole column of cards.
	def numValidDescending(self,col:int,row:int) -> int:
		"""Returns the number of valid descending cards.

		Args:
			col (int): column to check
			row (int): row to check

		Returns:
			int: Returns 1 if this is the bottom most card,
			or more if there are more descending cards below it.
			If a column is clicked such as [8, 7, 9], will return 0
			as this is not a valid descending column. Therefore
			a valid column will ALWAYS be >0.
		"""
		colToCheck:List[Card] = self.columns[col]
		maxVal = colToCheck[row].value+1

		for i in range(row,len(colToCheck)):
			#print(f"{colToCheck[i].value} < {maxVal}?")
			if colToCheck[i].value < maxVal:
				maxVal = colToCheck[i].value
			else:
				return 0
		return len(colToCheck)-row
	
	def checkAndMoveCompletedColumn(self, col:int) -> bool:

		columnToCheck = self.columns[col]
		start = len(columnToCheck)-1
		stop = start-13
		val = 1
		print("Checking completions: ",end='')
		for row in range(start, stop, -1):
			if columnToCheck[row].value == val and columnToCheck[row].faceUp:
				val+=1
				print(str(columnToCheck[row].value)+", ",end="")
			else:
				print("")
				return False
		print("Completed!")
		print("Removing cards from column "+str(col))
		# if we got this far, it was completed!
		for row in range(start, stop, -1):
			columnToCheck.pop()
		self.completedColumns += 1
		return True
	
	def isGameWon(self):
		return self.completedColumns == 8



# def debug_generate(card_type:TYPE):
# 	gen = []*13
# 	for i in range(1,13):
# 		gen[i] = Card(i,card_type,True)