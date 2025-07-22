from algos import NewtonRaphson
from math import pi, e, sqrt, log, sin, cos, atan

# Universal gravitational constant
G: float = 6.67428e-11
RADIANS: float = pi / 180
DEGREES: float = 180 / pi

REF_GRAVITY: float = 9.81
DEFAULT_ITER: int = 100000
ECCENTRIC_ANOMALY_TOLERANCE: float = 1E-5 * RADIANS

def approxEccentricAnomaly(mean_anomaly: float, ecc: float) -> float:
	return mean_anomaly + ecc * sin(mean_anomaly)

def KeplerEquation(eccentric_anomaly: float, ecc: float) -> float:
	return eccentric_anomaly - ecc * sin(eccentric_anomaly)

def KeplerPrime(eccentric_anomaly: float, ecc: float) -> float:
	return 1.0 - ecc * cos(eccentric_anomaly)

def trueAnomaly(mean_anomaly: float, ecc: float) -> float:
	eccentric_anomaly: float = NewtonRaphson(mean_anomaly, ecc, KeplerEquation, KeplerPrime, approxEccentricAnomaly(mean_anomaly, ecc), ECCENTRIC_ANOMALY_TOLERANCE, DEFAULT_ITER)

	beta_: float = ecc / (1.0 + sqrt(1.0 - ecc**2))
	nu_: float = eccentric_anomaly + 2.0 * atan((beta_*sin(eccentric_anomaly)) / (1.0 - beta_ * cos(eccentric_anomaly)))

	return nu_

def ln(x: float) -> float:
	return log(x, e)

def deltaV(dry_mass: float, wet_mass: float, isp: float, gravity: float=REF_GRAVITY) -> float:
	return ln(wet_mass / dry_mass) * isp * gravity

def stdGravParam(mass: float) -> float:
	"""Returns the gravitational parameter of a specific mass"""
	return mass * G

def meanMotion(mass: float, Mass: float, sma: float) -> float:
	mu: float = stdGravParam(mass) + stdGravParam(Mass)

	return sqrt(mu / sma**3)

def meanAnomalyAtUT(mass: float, Mass: float, sma: float, mean_anomaly: float, epoch: float, UT: float) -> float:
		mean_motion: float = meanMotion(mass, Mass, sma)

		mean_ano_UT: float = mean_anomaly + (UT - epoch) * mean_motion
		mean_ano_UT %= 2 * pi

		return mean_ano_UT

def orbitalPeriod(mass: float, Mass: float, sma: float) -> float:
	mu: float = stdGravParam(mass) + stdGravParam(Mass)

	return 2 * pi * sqrt(sma ** 3 / mu)

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

def orbitalSpeed_Elliptical(mass: float, Mass: float, altitude: float, sma: float) -> float:
	mu: float = stdGravParam(mass) + stdGravParam(Mass)

	return sqrt(mu * (2.0 / altitude - 1.0 / sma))

def orbitalSpeed_Circular(mass: float, Mass: float, sma: float) -> float:
	return orbitalSpeed_Elliptical(mass, Mass, sma, sma)

def orbitalSpeed_Parabolic(mass: float, Mass: float, altitude: float) -> float:
	mu: float = stdGravParam(mass) + stdGravParam(Mass)

	return sqrt(mu * (2.0 / altitude))

def orbitalSpeed_Hyperbolic(mass: float, Mass: float, altitude: float, sma: float) -> float:
	mu: float = stdGravParam(mass) + stdGravParam(Mass)

	return sqrt(mu * (2.0 / altitude + 1.0 / sma))
