class Card:
	def __init__(self, value:int, suit:int, faceUp:bool):
		# spade: 0, heart: 1, club: 2, diamond: 3
		self.value = value
		self.suit = suit
		self.faceUp = faceUp
		
class Column:
	def __init__(self, location:int, stack:Card):
		self.location = location
		self.stack = stack
	
class CardManager:
    def __init__(self, deck):
        self.deck = deck
        
    def createDeck(self):
    # make a deck with each card in it
        for x in range[13]:
            for y in range [4]:
                self.deck[x+13*(y)] = Card(x, y, 0)
                