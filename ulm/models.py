import kenlm

class CharLM(object):
    def __init__(self, lm_file, vocab_file, eos='</s>'):
        self.lm_file = lm_file
        self.vocab_file = vocab_file
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

    def __repr__(self):
        return 'CharLM(lm={}, vocab={})'.format(self.lm_file, self.vocab_file)


class TokenLM(object):
    def __init__(self, lm_file, vocab_file, eos='</s>'):
        self.lm_file = lm_file
        self.vocab_file = vocab_file
        self.lm = kenlm.LanguageModel(lm_file)
        self.vocab = set(l.strip() for l in open(vocab_file) if l.strip())
        self.eos = eos

    def predict(self, hist):
        predictions = {}
        for w in self.vocab:
            if w == self.eos:
                logp = list(self.lm.full_scores(hist.strip()))[-1][0]
                predictions[self.eos] = logp
            else:
                logp = list(self.lm.full_scores(hist + w))[-2][0]
                predictions[w + ' '] = logp

        return predictions

    def __repr__(self):
        return 'TokenLM(lm={}, vocab={})'.format(self.lm_file, self.vocab_file)













