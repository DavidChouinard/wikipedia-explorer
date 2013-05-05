import argparse, pickle, pprint

def main(args):
    # number of popular articles requested is in args.size, default is 10
    graph = pickle.load(open(args.data, 'rb'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument('size', nargs='?', default=10, help="number of popular articles to return")
    main(parser.parse_args())
