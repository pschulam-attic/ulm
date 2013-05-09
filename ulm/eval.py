import argparse
import heapq
import logging
import math
import sys
from ulm.models import CharLM, TokenLM

def log_add(*ps):
    m = max(ps)
    return m + math.log10(sum(10 ** (p - m) for p in ps))


def get_consistent_predictions(predictions, suffix):
    for pred, log_p in predictions.iteritems():
        if suffix.startswith(pred):
            yield pred, log_p


def evaluate1(lm, test_data):
    assert hasattr(lm, 'predict')

    log_likelihoods = [-float('inf')] * (len(test_data)+2)
    log_likelihoods[0] = 0.0
    histories = []
    heapq.heappush(histories, (0, ''))

    while len(histories) > 0:
        s, hist = heapq.heappop(histories)
        logging.debug('Pop (%d, %s)', s, hist)
        
        if s < len(test_data):
            predictions = lm.predict(hist)
            for pred, log_p in get_consistent_predictions(predictions, test_data[s:]):
                e = s + len(pred)
                log_likelihoods[e] = log_add(log_likelihoods[e], log_p)
                logging.debug('\tP( %s | .... %s )= %.3f', pred, hist[-5:], log_p)
                new_hist = hist + pred
                heapq.heappush(histories, (len(new_hist), new_hist))

    log_likelihoods[-1] = lm.predict(test_data)[lm.eos]
    return sum(log_likelihoods)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Use a token language model', action='store_true')
    parser.add_argument('--lm', help='Load this language model file')
    parser.add_argument('--vocab', help='Use this vocabulary')
    parser.add_argument('--debug', help='Verbose output', action='store_true')
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format='%(message)s')

    LanguageModel = TokenLM if args.token else CharLM
    lm = LanguageModel(args.lm, args.vocab)
    logging.info('Evaluating %s', lm)
    test_data = [l.strip() for l in sys.stdin]
    logging.info('Testing on %d sentences', len(test_data))
    for i, sentence in enumerate(test_data):
        logging.info('\n%s', sentence)
        ll = evaluate1(lm, sentence)
        logging.info('LL= %.3f', ll)


if __name__ == '__main__':
    main()
