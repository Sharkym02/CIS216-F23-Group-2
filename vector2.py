# Class to handle x/y coords

class Vector2():
	def __init__(self,x:int=0,y:int=0) -> None:
		self.x:int = x
		"""The x coordinate"""

		self.y:int = y
		"""The y coordinate"""

	def IsPositive(self):
		return self.x >= 0 and self.y >= 0

	def __str__(self) -> str:
		return f"({self.x}, {self.y})"