def AntecedentDroite(a: float, b: float, y: float) -> float:
	return (y - b) / a

def NewtonRaphson(target, func_param, func, func_prime, x_start: float, tolerance: float, max_iter: int) -> float:
	xf = 0
	x_guess = x_start

	low_limit = target - tolerance
	high_limit = target + tolerance

	n: int = 0

	while (n < max_iter) and not ((low_limit <= func(x_guess, func_param)) and (func(x_guess, func_param) <= high_limit)):
		a = func_prime(x_guess, func_param)
		b = -func_prime(x_guess, func_param)*x_guess + func(x_guess, func_param)

		x_guess = AntecedentDroite(a, b, target)

		n += 1

	xf = x_guess

	return xf