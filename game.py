from __future__ import annotations

from physics import *

class Body:
	def __init__(self, name: str, mass: str, radius: str, sma: str, parent: None | Body):
		self.name: None | str = name

		self.mass: float = mass
		self.radius: float = radius

		self.sma: float = sma
		self.parent: None | Body = parent

	def computeComplementary(self):
		if (self.parent != None):
			self.SOI: float = sphereOfInfluence(self.mass, self.parent.mass, self.sma)

