import argparse
import os
import re

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
    parser.add_argument('data_dir', help='Absolute or relative path to brown corpus data')
    parser.add_argument('--chars', help='Produce character data not token data', action='store_true')
    args = parser.parse_args()

    data_files = [fn for fn in os.listdir(args.data_dir) if re.match('^c[a-z][0-9]{2}$', fn)]
    data_files = [os.path.join(args.data_dir, fn) for fn in data_files]

    sentences = []
    for fn in data_files:
        with open(fn) as stream:
            sentences.extend(list(clean_brown_file(stream)))

    if args.chars:
        sentence_chars = [char_explode(s) for s in sentences]
        sentences = [s for s in sentence_chars if s]

    print '\n'.join(sentences) + '\n'

if __name__ == '__main__':
    main()

















