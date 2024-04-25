import argparse
from .server import start_server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="File serving directory")
    args = parser.parse_args()

    start_server(args.directory)


if __name__ == "__main__":
    main()
