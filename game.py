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

			self.inc_degs: float = orbital.get("inc")
			self.arg_degs: float = orbital.get("arg")
			self.an_degs: float = orbital.get("an")

			self.inc: float = self.inc_degs * RADIANS
			self.arg: float = self.arg_degs * RADIANS
			self.an: float = self.an_degs * RADIANS

			self.mean_anomaly: float = orbital.get("mean_anomaly")

		# Loading atmospheric characteristics
		self.has_atmosphere: None | bool = atmospheric.get("has_atmosphere")

		if (self.has_atmosphere):
			self.pressure: float = atmospheric.get("pressure")
			self.atmosphere_height: float = atmospheric.get("height")
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

	def __dict__(self) -> str:
		output: dict = {
			"name": self.name,
			"physical": {},
			"atmospheric": {},
			"orbital": {}
		}

		# Filling in physical characteristics
		physical: dict = {
			"radius": self.radius,
			"mass": self.mass,
			"sidereal_day": self.sidereal_day,
			"solar_day": self.solar_day
		}

		# Filling in atmospheric characteristics
		if (self.has_atmosphere):
			atmospheric: dict = {
				"has_atmosphere": self.has_atmosphere,
				"pressure": self.pressure,
				"height": self.atmosphere_height,
				"temp_min": self.temp_min,
				"temp_max": self.temp_max,
				"has_oxygen": self.has_oxygen
			}
		else:
			atmospheric: dict = {
				"has_atmosphere": self.has_atmosphere
			}

		# Filling in physical characteristics
		if (self.has_parent):
			orbital: dict = {
				"has_parent": self.has_parent,
				"parent": self.parent_name,
				"sma": self.sma,
				"ecc": self.ecc,
				"inc": self.inc_degs,
				"arg": self.arg_degs,
				"an": self.an_degs,
				"mean_anomaly": self.mean_anomaly
			}
		else:
			orbital: dict = {
				"has_parent": self.has_parent
			}

		output["physical"] = physical
		output["atmospheric"] = atmospheric
		output["orbital"] = orbital

		return output

class Resource:
	def __init__(self, name: str, density: float, unit_cost: int):
		self.name: str = name
		self.density: str = density
		self.cost: str = unit_cost

class Fuel(Resource):
	def __init__(self, name: str, density: float, unit_cost: int):
		super().__init__(name, density, unit_cost)

class FuelMix:
	def __init__(self):
		self.fuels: dict[Fuel: float] = dict()

	def addFuel(self, fuel: Fuel, mass_ratio: float) -> None:
		self.fuels[fuel] = mass_ratio

class Part:
	def __init__(self, name: str, mass: float, cost: int):
		self.name: str = name
		self.mass: float = mass
		self.cost: int = cost

class Subtank:
	def __init__(self, resource: Resource, capacity: float, quantity: float):
		self.resource: Resource = resource
		self.capacity: float = capacity
		self.quantity: float = quantity

	def getResourceMass(self) -> float:
		return self.resource.density * self.quantity

	def getResourceValue(self) -> float:
		return self.resource.cost * self.quantity

	def isEmpty(self) -> bool:
		return self.quantity == 0.0

class Engine(Part):
	def __init__(self, name: str, mass: float, cost: int, fuel_mix: FuelMix, isp: int, thrust_vac: float, thrust_sea: float):
		super().__init__(name, mass, cost)

		self.fuel_mix: FuelMix = fuel_mix

		self.isp: int = isp
		self.thrust_vac: float = thrust_vac
		self.thrust_sea: float = thrust_sea

		self.thrust_pct: float = 100.0
		self.current_thrust: float = self.thrust_vac * self.thrust_pct/100.0

	def setThrustPct(self, pct: float) -> float:
		self.thrust_pct = pct
		self.current_thrust = self.thrust_vac * self.thrust_pct/100.0

		return self.current_thrust

	def computePct(self, thrust: float) -> float:
		pct: float = thrust / self.thrust_vac * 100.0

		if (pct > 100.0):
			pct = 100.0
		elif (pct < 0.0):
			pct = 0.0

		self.setThrustPct(pct)

		return pct

class Tank(Part):
	def __init__(self, name: float, dry_mass: float, cost: int):
		super().__init__(name, dry_mass, cost)

		self.subtanks: set[Subtank] = set()

	def getResources(self) -> set[Resource]:
		resources: set[Resource] = set()

		for subtank in self.subtanks:
			resources.add(subtank.resource)

		return resources

	def getRemainingResources(self) -> set[Resource]:
		resources: set[Resource] = set()

		for subtank in self.subtanks:
			if (not subtank.isEmpty()):
				resources.add(subtank.resource)

		return resources

	def addSubtank(self, subtank: Subtank) -> None:
		self.subtanks.add(subtank)

	def getTotalResourcesValues(self) -> float:
		sum: float = 0.0

		for subtank in self.subtanks:
			sum += subtank.getResourceValue()

		return sum

	def getTotalCost(self) -> float:
		return self.cost + self.getTotalResourcesValues()

