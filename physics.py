from math import *

# Universal gravitational constant
G: float = 6.67428e-11
RADIANS: float = pi / 180
DEGREES: float = 180 / pi

REF_GRAVITY: float = 9.81

def ln(x: float) -> float:
	return log(x, e)

def deltaV(dry_mass: float, wet_mass: float, isp: float, gravity: float=REF_GRAVITY) -> float:
	return ln(wet_mass / dry_mass) * isp * gravity

def stdGravParam(mass: float) -> float:
	"""Returns the gravitational parameter of a specific mass"""
	return mass * G

def sphereOfInfluence(mass: float, Mass: float, distance: float) -> float:
	"""Returns the SOI's radius of a given mass"""

	distance = abs(distance)

	if (distance == 0.0):
		return float("inf")

	return distance * (mass / Mass) ** (2/5)

def smaFromPeriod(mass: float, Mass: float, period: float) -> float:
	output: float = period / (2 * pi)
	output **= 2
	output *= stdGravParam(mass) + stdGravParam(Mass)
	output **= 1/3

	return output

def apoapsis(sma: float, ecc: float) -> float:
	return sma * (1.0 + ecc)

def periapsis(sma: float, ecc: float) -> float:
	return sma * (1.0 - ecc)

