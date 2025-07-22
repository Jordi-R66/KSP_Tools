from game import Body
from parser import parseBodies

bodies = parseBodies("stock.json")

print(Body.BODIES["Kerbin"])