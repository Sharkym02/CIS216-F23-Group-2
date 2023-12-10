#!/usr/bin/env python3
import unittest
from unittest import mock
from gamelogic import Card, SpiderGame
from vector2 import Vector2
#from main im

class UnitTestCard(unittest.TestCase):

	def test_deck(self):
		self.assertEqual(len(SpiderGame.createDeck()),52,
			"Size of deck is improper")
	
	def test_game_generation(self):
		spider = SpiderGame()
		self.assertEqual(
			len(spider.columns),
			SpiderGame.NUM_COLUMNS,
			"Spider didn't generate defined number of columns in const")
		spider.startNewGame()
		self.assertEqual(
			len(spider.columns),
			SpiderGame.NUM_COLUMNS,
			"Resetting columns failed!")
		
	def test_move(self):
		spider = SpiderGame()
		print(spider.debug_print_game())
		c:Card = spider.columns[0][-1]
		col,row = 0,len(spider.columns[0])-1
		for i in range(1,len(spider.columns)):
			dstCard:Card = spider.columns[i][-1]
			if dstCard.value == c.value+1 and dstCard.faceUp:
				self.assertTrue(
					spider.tryMoveCards(col,row,i,len(spider.columns[i])-1),
					f"Could not move card {c.value} ({col},{row}) on top of another card {dstCard.value}"
				)
				break
		
		
		c:Card = spider.columns[0][-1]
		col,row = 0,len(spider.columns[0])-1
		#Clear column 1
		spider.columns[1] = []
		self.assertTrue(
			spider.tryMoveCards(col,row,1,0),
			f"Could not move card {c.value} into empty column at idx 1"
		)

	def test_vector2(self):
		vec2 = Vector2(-1,-1)
		self.assertFalse(vec2.IsPositive(),"Vector2 should not be positive")

if __name__ == "__main__":
	unittest.main()