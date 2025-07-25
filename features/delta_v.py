from math import *
from game import Orbit, Body, Craft
from physics import *

def changeInclinationAtUT(orbit: Orbit, new_inclination: float, UT: float) -> float:
	DeltaI: float = (new_inclination - orbit.inc_degs) * RADIANS
	vel: float = orbit.orbitalSpeedAtUT(UT)

	DeltaV: float = 2.0 * vel * sin(DeltaI / 2.0)

	if (orbit.orbit_class != Orbit.CIRCULAR):
		true_ano: float = orbit.trueAnomalyAtUT(UT)
		DeltaV *= (1.0 + orbit.ecc * cos(true_ano)) * orbit.meanMotion() * orbit.sma / (sqrt(1 - orbit.ecc**2) * cos(orbit.arg + true_ano))

	return DeltaV

def changeApoAtAltitude(orbit: Orbit, newApo: float) -> tuple[float, Orbit]:
	