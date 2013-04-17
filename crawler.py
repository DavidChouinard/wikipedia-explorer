import io, argparse

def main(args):
    start = io.open(args.start_file, "r")

def crawl():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start_file", help="initial file to start crawling")
    args = parser.parse_args()

    main(args)
