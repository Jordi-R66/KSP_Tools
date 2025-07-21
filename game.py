from __future__ import annotations

from physics import *

class Body:
	BODIES: dict = dict()

	def __init__(self, name: str, physical: dict, orbital: dict):
		self.name: None | str = name

		# Loading physical characteristics
		self.mass: float = physical.get("mass")
		self.radius: float = physical.get("radius")
		self.sidereal_day: float = physical.get("sidereal_day")
		self.solar_day: float = physical.get("solar_day")

		# Loading orbital parameters
		self.has_parent: None | bool = orbital.get("has_parent")

		if (self.has_parent):
			self.parent_name: None | str = orbital.get("parent")

			self.sma: float = orbital.get("sma")
			self.ecc: float = orbital.get("ecc")

			self.inc: float = orbital.get("inc") * pi / 180
			self.arg: float = orbital.get("arg") * pi / 180
			self.an: float = orbital.get("an") * pi / 180

			self.mean_anomaly: float = orbital.get("mean_anomaly")

