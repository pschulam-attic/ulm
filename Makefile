SHELL=/bin/bash

CHARORDER=12
TOKENORDER=5

char.lm: data/train.char.txt
	ngram-count -text $< -order $(CHARORDER) -unk -write-vocab char_vocab.txt -wbdiscount -lm $@

token.lm: data/train.token.txt data/test.txt
	cat $^ | sort | uniq > token_vocab.txt
	echo '<s>' >> token_vocab.txt
	echo '</s>' >> token_vocab.txt
	ngram-count -text $< -order $(TOKENORDER) -unk -vocab token_vocab.txt -interpolate -kndiscount -lm $@

clean:
	rm -f char.lm

.PHONY: clean
