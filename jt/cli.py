import json
import argparse
from pprint import pprint

from typing import List, Dict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="A useful tool for json file.")
    parser.add_argument("file", help="file path", type=Path)
    parser.add_argument(
        "--description",
        "-d",
        action="store_true",
        default=False,
        help="print descriptions of the file, including num of examples and data structure.",
    )
    parser.add_argument(
        "--structure",
        "-s",
        action="store_true",
        default=False,
        help="print data structure",
    )
    parser.add_argument(
        "--key", type=str, default=None, help="select key. e.g. 'a.b.c'"
    )
    parser.add_argument(
        "--value_set",
        default=False,
        action="store_true",
        help="print the value set of the key.",
    )
    parser.add_argument(
        "--print_example",
        "-e",
        default=False,
        action="store_true",
        help="ppring an example.",
    )
    parser.add_argument("--index", type=int, default=0, help="selected example index.")
    return parser.parse_args()


def print_key_tree(data, indent=1):
    if isinstance(data, List):
        print("...." * indent, "[")
        print_key_tree(data[0], indent + 1)
        print("...." * indent, "]")
    elif isinstance(data, Dict):
        for key in data.keys():
            print("...." * indent, key)
            print_key_tree(data[key], indent + 1)


def print_description(dataset):
    if isinstance(dataset, List):
        print(f"The file has {len(dataset)} examples.")
    print("The file structure is:")
    print_key_tree(dataset)


def process_jsonl(args):
    f = open(args.file, "r")
    if args.description:
        dataset = [json.loads(line) for line in f.readlines()]
        print_description(dataset[0])
    elif args.structure:
        print_key_tree(json.loads(f.readline()))
    elif args.print_example:
        for i, line in enumerate(f):
            if i == args.index:
                pprint(json.loads(line))

    f.close()


def process_json(args):
    f = open(args.file, "r")
    dataset = json.load(f)
    if args.description or args.structure:
        print_description(dataset)
    elif args.structure:
        print_key_tree(dataset)
    elif args.print_example:
        pprint(dataset[args.index])

    f.close()


def main():
    args = parse_args()
    if args.file.suffix == ".jsonl":
        process_jsonl(args)
    elif args.file.suffix == ".json":
        process_json(args)
    else:
        raise NotImplementedError("Only support json and jsonl file.")


if __name__ == "__main__":
    main()
