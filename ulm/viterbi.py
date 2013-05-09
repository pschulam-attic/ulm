import operator
from collections import namedtuple


Edge = namedtuple('Edge', ['start', 'end', 'weight'])


Semiring = namedtuple('Semiring', ['zero', 'one', 'plus', 'times'])


tropical_semiring = Semiring(float('inf'), 0, min, operator.add)










