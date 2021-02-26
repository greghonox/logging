from logging import handlers,  Formatter, getLogger, StreamHandler
from logging.handlers import RotatingFileHandler
from random import randint
import doctest

def printf(msg, tipo=1):
	tipos = {1: 'critical', 2: 'warning', 3: 'error'}
	t = {1: 'CRITICAL', 2: 'WARNING', 3: 'ERROR'}
	log = getLogger('MATEMATICA')
	log.setLevel(t[tipo])
	prin = StreamHandler()
	handler = RotatingFileHandler('/tmp/log.log', maxBytes=5000000, backupCount=5)
	handler.setFormatter(Formatter("%(asctime)s program_name [%(process)d]: %(message)s"))
	# prin.setFormatter(Formatter("%(asctime)s program_name [%(process)d]: %(message)s"))
	log.addHandler(handler)
	# log.addHandler(prin)
	eval(f"log.{tipos[tipo]}('{msg}')")

class Matematica:
	def __init__(self):
		...

	def soma(self, x, y):
		'''
			FAZ SOMA DE X + Y
			>>> Matematica().soma(3, 5)
			8
		'''
		printf(f"A SOMA DE {x} + {y} = {x + y} ", randint(1, 3))
		return x + y

doctest.testmod()

for _ in range(1000): Matematica().soma(randint(1, 100000), randint(1, 1000000))

