# Class to handle x/y coords

class Vector2():
	def __init__(self,x:float=0.0,y:float=0.0) -> None:
		self.x:float = x
		"""The x coordinate"""

		self.y:float = y
		"""The y coordinate"""

	def __str__(self) -> str:
		return f"({self.x}, {self.y})"