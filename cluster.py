import argparse, pickle, pprint

def main(args):
    graph = pickle.load(open(args.data, 'rb'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    main(parser.parse_args())
