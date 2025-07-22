from __future__ import annotations

from physics import RADIANS, deltaV, meanAnomalyAtUT, sphereOfInfluence, apoapsis, periapsis, smaFromPeriod, orbitalSpeed_Circular, orbitalSpeed_Elliptical, orbitalSpeed_Parabolic, orbitalSpeed_Hyperbolic, trueAnomaly, altitudeFromTrueAnomaly

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
		self.orbit: Orbit | None = None

		if (self.has_parent):
			self.parent_name: None | str = orbital.get("parent")

			sma: float = orbital.get("sma")
			ecc: float = orbital.get("ecc")

			inc_degs: float = orbital.get("inc")
			arg_degs: float = orbital.get("arg")
			an_degs: float = orbital.get("an")

			mean_anomaly: float = orbital.get("mean_anomaly")
			epoch: float = orbital.get("epoch")

			self.orbit = Orbit(self.mass, None, sma, ecc, inc_degs, arg_degs, an_degs, mean_anomaly, epoch)

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
				self.orbit.parent_mass = self.parent.mass
			else:
				raise Exception(f"Couldn't find body named \"{self.parent_name}\"")

			self.orbit.getOrbitClass()

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

	def getMass(self):
		return self.mass

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

	def getMass(self) -> float:
		return self.mass

class Tank(Part):
	def __init__(self, name: float, dry_mass: float, cost: int):
		super().__init__(name, dry_mass, cost)

		self.subtanks: set[Subtank] = set()

	def addSubtank(self, subtank: Subtank) -> None:
		self.subtanks.add(subtank)

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

	def getRemainingMasses(self) -> dict[Resource: float]:
		resources: dict[Resource: float] = dict()

		for subtank in self.subtanks:
			if (not subtank.isEmpty()):
				resources[subtank.resource] = subtank.getResourceMass()

		return resources

	def getTotalResourcesCost(self) -> float:
		value: float = 0.0

		for subtank in self.subtanks:
			value += subtank.getResourceValue()

		return value

	def getMass(self) -> float:
		return self.mass + sum(self.getRemainingMasses().values())

	def getTotalCost(self) -> float:
		return self.cost + self.getTotalResourcesCost()

class Stage:
	def __init__(self):
		self.parts: set[Part] = set()

	def getTanks(self) -> set[Tank]:
		tanks: set[Tank] = set()

		for part in self.parts:
			if type(part) == Tank:
				tanks.add(part)

		return tanks

	def getEngines(self) -> set[Engine]:
		engines: set[Engine] = set()

		for part in self.parts:
			if type(part) == Engine:
				engines.add(part)

		return engines

	def getMass(self) -> float:
		mass: float = 0.0

		for part in self.parts:
			mass += part.getMass()

		return mass

	def getWorkingEngines(self) -> set[Engine]:
		tanks: set[Tank] = self.getTanks()
		engines: set[Engine] = self.getEngines()

		working_engines: set[Engine] = set()
		available_fuels: set[Resource] = set()

		for tank in tanks:
			tank_resources: set[Resource] = tank.getRemainingResources()

			for resource in tank_resources:
				if not (type(resource) == Fuel):
					tank_resources.remove(resource)

			available_fuels.update(tank_resources)

		for engine in engines:
			fuel_mix: FuelMix = engine.fuel_mix
			fuels: set[Fuel] = set(fuel_mix.fuels.keys())

			if (len(fuels) == available_fuels.intersection(fuels)):
				working_engines.add(engine)

		return working_engines

	def getBurnableFuelMass(self) -> float:
		tanks: set[Tank] = self.getTanks()
		engines: set[Engine] = self.getWorkingEngines()

		burnable_mass: float = 0.0
		fuel_burned: set[Fuel] = set()

		for engine in engines:
			fuel_burned.update(set(engine.fuel_mix.fuels.keys()))

		for tank in tanks:
			tank_masses: dict[Resource: float] = tank.getRemainingMasses()

			for resource, mass in tank_masses.items():
				if (type(resource) == Fuel) and (resource in fuel_burned):
					burnable_mass += mass

		return burnable_mass

	def getStageDeltaV(self) -> float:
		engines: set[Engine] = self.getWorkingEngines()

		ThrustSum: float = 0.0
		RatioSum: float = 0.0

		for engine in engines:
			ThrustSum += engine.current_thrust
			RatioSum += engine.current_thrust / engine.isp

		stage_isp: float = ThrustSum / RatioSum
		burnable_mass: float = self.getBurnableFuelMass()

		total_mass: float = self.getMass()
		dry_mass: float = total_mass - burnable_mass

		delta_v: float = deltaV(dry_mass, total_mass, stage_isp)

		return delta_v

class Craft:
	def __init__(self):
		self.stages: list[Stage] = []

	def addStages(self, stages: list[Stage]):
		self.stages += stages

class Orbit:
	CIRCULAR: str = "CIRCULAR"
	ELLIPTICAL: str = "ELLIPTICAL"
	PARABOLIC: str = "PARABOLIC"
	HYPERBOLIC: str = "HYPERBOLIC"

	def __init__(self, object_mass: float, parent_mass: float, sma: float, ecc: float, inc: float, arg: float, an: float, mean_ano: float, epoch: float = 0.0):
		self.obj_mass: float = object_mass
		self.parent_mass: float = parent_mass

		self.sma: float = sma
		self.ecc: float = ecc

		self.inc_degs: float = inc
		self.arg_degs: float = arg
		self.an_degs: float = an

		self.inc: float = inc * RADIANS
		self.arg: float = arg * RADIANS
		self.an: float = an * RADIANS

		self.mean_anomaly: float = mean_ano
		self.epoch = epoch

		self.orbit_class: str = None

	def getOrbitClass(self) -> str:
		if (self.ecc == 0.0):
			self.orbit_class = Orbit.CIRCULAR
		elif (self.ecc < 1.0):
			self.orbit_class = Orbit.ELLIPTICAL
		elif (self.ecc == 1.0):
			self.orbit_class = Orbit.PARABOLIC
		elif (self.ecc > 1.0):
			self.orbit_class = Orbit.HYPERBOLIC
		else:
			raise Exception("Eccentricity must be >= 0")

		return self.orbit_class

	def meanAnomalyAtUT(self, UT: float) -> float:
		return meanAnomalyAtUT(self.obj_mass, self.parent_mass, self.sma, self.mean_anomaly, self.epoch, UT)

	def orbitalSpeedAtAltitude(self, altitude: float) -> float:
		match (self.orbit_class):
			case Orbit.CIRCULAR:
				return orbitalSpeed_Circular(self.obj_mass, self.parent_mass, self.sma,)

			case Orbit.ELLIPTICAL:
				return orbitalSpeed_Elliptical(self.obj_mass, self.parent_mass, altitude, self.sma)

			case Orbit.PARABOLIC:
				return orbitalSpeed_Parabolic(self.obj_mass, self.parent_mass, altitude)

			case Orbit.HYPERBOLIC:
				return orbitalSpeed_Hyperbolic(self.obj_mass, self.parent_mass, altitude, self.sma)

			case _:
				raise Exception("Couldn't identify current orbit class")

	def altitudeAtUT(self, UT: float) -> float:
		mean_ano: float = self.meanAnomalyAtUT(UT)
		true_anomaly: float = trueAnomaly(mean_ano, self.ecc)

		return altitudeFromTrueAnomaly(self.ecc, self.sma, true_anomaly)

	def orbitalSpeedAtUT(self, UT: float) -> float:
		altitude: float = self.altitudeAtUT(UT)

		return self.orbitalSpeedAtAltitude(altitude)
