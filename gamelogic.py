import random

class Card:
	def __init__(self, value:int, suit:int, faceUp:bool):
		# spade: 0, heart: 1, club: 2, diamond: 3
		self.value = value
		self.suit = suit
		self.faceUp = faceUp

	
class CardManager:
	# The end of the list is the top of the deck
	# The beginning of the list is the bottom of the deck
	def __init__(self, deck: list):
		self.deck = deck
        
	def createDeck(self):
    # make a deck with each card in it
		for x in range(1, 14):
			for y in range(4):
				self.deck[x+13*(y)] = Card(x, y, 0)

	def reset(self):
		self.deck.clear()
		self.createDeck()
                
	def popTop(self):
		last = self.deck.pop(-1)
		return last
	
	def popTop(self):
		first = self.deck.pop(0)
		return first
	
	def addTop(self, card: Card):
		self.deck.append(card)

	def addBottom(self, card: Card):
		self.deck.insert(card)

	def shuffle(self):
		random.shuffle(self.deck)

class Column(CardManager):
	def __init__(self, location, *args, **kwargs):
		Column.__init__(self, location, *args, **kwargs)