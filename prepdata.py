import argparse
import sys

def clean_brown_sentence(sentence):
    words = [w.split('/')[0] for w in sentence.split()]
    return ' '.join(words)

def clean_brown_file(stream):
    sentences = [l.strip() for l in stream if l.strip()]
    for sentence in sentences:
        words = [w.split('/')[0] for w in sentence.split()]
        yield ' '.join(words)

def char_explode(sentence):
    chars = []
    for c in sentence:
        if c == ' ':
            chars.append('<space>')
        else:
            chars.append(c)
    return ' '.join(chars)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chars', help='Produce character data not token data', action='store_true')
    args = parser.parse_args()

    for line in sys.stdin:
        sentence = clean_brown_sentence(line.strip())
        if args.chars:
            print char_explode(sentence)
        else:
            print sentence

if __name__ == '__main__':
    main()

















