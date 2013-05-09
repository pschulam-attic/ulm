import argparse
import random
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help='Percentage of data for training', type=float)
    parser.add_argument('--train', help='Write the training data to this file', default='train.txt')
    parser.add_argument('--test', help='Write the test data to this file', default='test.txt')
    parser.add_argument('--seed', help='Random seed (a string)', default='split')
    args = parser.parse_args()

    data = [l.strip() for l in sys.stdin if l.strip()]
    random.seed(args.seed)
    train_set = set(random.sample(xrange(len(data)), int(args.p * len(data))))

    with open(args.train, 'w') as train, open(args.test, 'w') as test:
        for i, d in enumerate(data):
            stream = train if i in train_set else test
            stream.write(d + '\n')


if __name__ == '__main__':
    main()

















