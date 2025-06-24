from math import *

# Universal gravitational constant
G: float = 6.67428e-11

def stdGravParam(mass: float) -> float:
	"""Returns the gravitational parameter of a specific mass"""
	return mass * G

def sphereOfInfluence(mass: float, Mass: float, distance: float) -> float:
	"""Returns the SOI's radius of a given mass"""

	distance = abs(distance)

	if (distance == 0.0):
		return float("inf")

	return distance * (mass / Mass) ** (2/5)
