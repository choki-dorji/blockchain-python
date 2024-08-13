import argparse
import asyncio

from druk.p2p.node import start_node


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='Host name')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        asyncio.run(start_node(args.host, args.port))
    except KeyboardInterrupt:
        print("Keyboard interrupt")


if __name__ == "_main_":
    main()