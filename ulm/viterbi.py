import math
import operator
from collections import namedtuple

def log_add(*ps):
    m = max(ps)
    return m + math.log10(sum(10 ** (p - m) for p in ps))

Edge = namedtuple('Edge', ['start', 'end', 'weight'])

Semiring = namedtuple('Semiring', ['zero', 'one', 'plus', 'times'])
tropical_semiring = Semiring(float('inf'), 0, min, operator.add)
log_prob_semiring = Semiring(-float('inf'), 0, log_add, operator.add)


def forward(graph, incoming_edges, semiring):
    node_score = {}
    node_score[graph[0]] = semiring.one
    for i in xrange(1, len(graph)):
        node = graph[i]
        node_score[node] = semiring.zero
        for edge in incoming_edges[node]:
            score = semiring.times(node_score[edge.start], edge.weight)
            node_score[node] = semiring.plus(node_score[node], score)
    return node_score
