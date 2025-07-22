from __future__ import annotations

from physics import RADIANS, DEGREES, sphereOfInfluence, apoapsis, periapsis, smaFromPeriod
from pprint import pprint

class Body:
	BODIES: dict = dict()

	def __init__(self, name: str, physical: dict, orbital: dict, atmospheric: dict):
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

			self.inc: float = orbital.get("inc") * RADIANS
			self.arg: float = orbital.get("arg") * RADIANS
			self.an: float = orbital.get("an") * RADIANS

			self.mean_anomaly: float = orbital.get("mean_anomaly")

		# Loading atmospheric characteristics
		self.has_atmosphere: None | bool = atmospheric.get("has_atmosphere")

		if (self.has_atmosphere):
			self.pressure: float = atmospheric.get("pressure")
			self.height: float = atmospheric.get("height")
			self.temp_min: float = atmospheric.get("temp_min")
			self.temp_max: float = atmospheric.get("temp_max")
			self.has_oxygen: bool = atmospheric.get("has_oxygen")

	def completeBody(self) -> None:
		self.SOI: float = float('inf')
		self.stationary: float | None = None

		if (self.has_parent):
			self.parent: Body = None

			if (self.parent_name in Body.BODIES.keys()):
				self.parent = Body.BODIES.get(self.parent_name)

			self.SOI = sphereOfInfluence(self.mass, self.parent.mass, self.sma)
			self.apo = apoapsis(self.sma, self.ecc)
			self.peri = periapsis(self.sma, self.ecc)

		self.stationary = smaFromPeriod(0, self.mass, self.sidereal_day)

		if (self.stationary > self.SOI):
			self.stationary = None

	def __str__(self) -> str:
		header: str = f"""{self.name}"""

		# PHYSICAL SECTION
		physical: str = f"RADIUS: {self.radius:,} meters\nMASS: {self.mass:.7e} kg\nSIDEREAL DAY: {self.sidereal_day:,.3f} secs"

		if not (self.solar_day is None):
			physical += f"\nSOLAR DAY: {self.solar_day:,.3f} secs"

		# ORBITAL SECTION
		if (self.has_parent):
			orbital: str = f"PARENT: {self.parent_name}\n\nSMA: {int(self.sma):,} meters\nECC: {self.ecc:.7f}\nINC: {self.inc * DEGREES:.2f} degs\nARG: {self.arg * DEGREES:.2f} degs\nAN: {self.an * DEGREES:.2f} degs\nMEAN ANO : {self.mean_anomaly * DEGREES:.2f} degs"
		else:
			orbital: str = f"NO PARENT BODY"

		sections: list[str] = [header, physical, orbital]
		output: str = f"\n{'-' * 45}\n".join(sections)

		return f"{output}\n\n"