import heapq
import kenlm

class Evaluator(object):
    def __init__(self, test_data):
        self.test_data = test_data
    
    def evaluate(self, lm):
        assert hasattr(lm, 'predict')

        log_likelihoods = [-float('inf')] * (len(self.test_data)+1)

        hist_heap = []
        heapq.heappush(hist_heap, (0, ''))

        while len(hist_heap) > 0:
            i, hist = heapq.heappop(hist_heap)
            if i < len(self.test_data):
                log_likelihoods[i] = lm.predict(hist)[self.test_data[i]]
                new_hist = hist + self.test_data[i]
                heapq.heappush(hist_heap, (len(new_hist), new_hist))
        log_likelihoods[-1] = lm.predict(self.test_data)[lm.eos]

        # for i in xrange(len(self.test_data)):
        #     hist = self.test_data[:i]
        #     log_likelihoods[i] = lm.predict(hist)[self.test_data[i]]
        # log_likelihoods[-1] = lm.predict(self.test_data)[lm.eos]

        return sum(log_likelihoods)


class CharLM(object):
    def __init__(self, lm_file, vocab_file, eos='</s>'):
        self.lm = kenlm.LanguageModel(lm_file)
        self.vocab = set(l.strip() for l in open(vocab_file))
        self.eos = eos

    def predict(self, hist):
        mod_hist = []
        for c in hist:
            if c == ' ':
                mod_hist.append('<space>')
            else:
                mod_hist.append(c)

        predictions = {}
        for w in self.vocab:
            hist = ' '.join(mod_hist + [w])
            logp = list(self.lm.full_scores(hist))[-2][0]
            w = ' ' if w == '<space>' else w
            predictions[w] = logp

        return predictions


class TokenLM(object):
    def __init__(self, lm_file, vocab_file, eos='</s>'):
        self.lm = kenlm.LanguageModel(lm_file)
        self.vocab = set(l.strip() for l in open(vocab_file) if l.strip())
        self.eos = eos

    def predict(self, hist):
        predictions = {}
        for w in self.vocab:
            logp = list(self.lm.full_scores(hist + w))[-2][0]
            predictions[w] = logp

        return predictions
