SHELL=/bin/bash
BROWN=/Users/pschulam/data/brown/
SPLITSEED=ngrams

TOKENORDER=5
CHARORDER=12

token.lm: token_train.txt
	cat token_train.txt token_test.txt | tr ' ' '\n' | sort | uniq > token_vocab.txt
	echo '<s>' >> token_vocab.txt
	echo '</s>' >> token_vocab.txt
	ngram-count -text $< -order $(TOKENORDER) -vocab token_vocab.txt -unk -lm $@

char.lm: char_train.txt
	ngram-count -text $< -order $(CHARORDER) -unk -write-vocab char_vocab.txt -wbdiscount -lm $@

token_train.txt:
	python prepdata.py $(BROWN) \
	| python train_test_split.py -p 0.75 --train $@ --test token_test.txt --seed $(SPLITSEED)

token_test.txt: token_train.txt

char_train.txt:
	python prepdata.py --chars $(BROWN) \
	| python train_test_split.py -p 0.75 --train $@ --test char_test.txt --seed $(SPLITSEED)

char_test.txt: char_train.txt

clean:
	rm -f {token,char}_{train,test}.txt
	rm -f {token,char}_vocab.txt
	rm -f {token,char}.lm

.PHONY: clean
