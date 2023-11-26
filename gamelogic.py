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
	
	@faceUp.setter # TODO: Somehow correctly set up setter for the faceUp value.
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
	def __init__(self):

		self.deck:List[Card] = []
		"""The deck of cards. In spider solitiare, there are two decks totalling 104."""
		self.columns:List[List[Card]] = []
		"""All the columns of the play area. There are 10 in total."""

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
		for i in range(10):
			self.columns.append([])


		#For four columns, move five cards into each column
		for col in range(4): #0,1,2,3
			for i in range(5):
				self.columns[col].append(self.deck.pop())

		#Repeat but now 4 cards
		for col in range(4,10): #4,5,6,7,8,9
			for i in range(4):
				self.columns[col].append(self.deck.pop())

		for col in range(10): # Placing faceup cards in all columns
			c = self.deck.pop()
			c.faceUp = True
			self.columns[col].append(c)

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


# def debug_generate(card_type:TYPE):
# 	gen = []*13
# 	for i in range(1,13):
# 		gen[i] = Card(i,card_type,True)