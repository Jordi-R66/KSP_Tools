from math import cos, sin, tan
from physics import DEGREES, RADIANS

from game import Orbit, Body, Craft

def angleBetweenNSatellites(nSatellites: int) -> float:
	"""Returns the angle relative to the center of the orbit separating N equally spaced satellites placed on the same CIRCULAR orbit"""
	return 360 / int(nSatellites)

def smaFromLineOfSightForNSatellites(body: Body, lineOfSight: float, nSatellites: float) -> float:
	"""This assumes a circular orbit for your constellation"""
	angle: float = angleBetweenNSatellites(nSatellites)
	sma: float = lineOfSight / (2 * sin( angle / 2 * RADIANS))

	if (sma <= body.safetyLimit):
		raise Exception(f"Orbit below safety limit of {body.safetyLimit} for \"{body.name}\"")
	else:
		return sma

def lineOfSightFromSmaForNSatellites(body: Body, sma: float, nSatellites: float) -> float:
	"""This assumes a circular orbit for your constellation"""
	angle: float = angleBetweenNSatellites(nSatellites)

	if (sma <= body.safetyLimit):
		raise Exception(f"Won't compute line of sight for a satellite under safety limit of {body.safetyLimit} for {body.name}")
	else:
		return 2 * sma * sin(angle / 2 * RADIANS)

def lineOfSightObstructedByBody(body: Body, sma: float, nSatellites: float) -> bool:
	"""This assumes a circular orbit"""
	los: float = lineOfSightFromSmaForNSatellites(body, sma, nSatellites)

	angle: float = angleBetweenNSatellites(nSatellites)
	half_angle: float = angle / 2
	half_FOV: float = 180 - 90 - half_angle

	los_tangent_dist: float = sin(half_FOV * RADIANS) * sma

	return los_tangent_dist <= body.commsOccluded

