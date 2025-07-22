from json import loads
from game import Body

def parseBodies(filename: str) -> list[Body]:
	output: list[Body] = []

	fp = open(filename, "r", encoding="utf-8")

	raw: str = fp.read()
	unparsed_data: dict[list[dict[str: str, str: [dict[str: float]], str: dict[str: bool, str: str, str: float]]]] = loads(raw)

	fp.close()

	for body_raw in unparsed_data["Bodies"]:
		name: str = body_raw["name"]

		physical: dict = body_raw["physical"]
		orbital: dict = body_raw["orbital"]
		atmospheric: dict = body_raw["atmospheric"]

		body: Body = Body(name, physical, orbital, atmospheric)

		output.append(body)
		Body.BODIES[name] = body

	for body in output:
		body.completeBody()

	return list(output)