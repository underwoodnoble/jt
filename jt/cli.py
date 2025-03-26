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
        "--new_key", default=None, type=str, help="new key to replace the key."
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


def get_value_by_key_list(data, key_list):
    if len(key_list) == 0:
        return data
    else:
        try:
            return get_value_by_key_list(data[key_list[0]], key_list[1:])
        except Exception:
            raise ValueError(f"Do not find value with key list: {key_list}")


def delete_value_by_key_list(data, key_list):
    try:
        if len(key_list) == 1:
            value = data[key_list[0]]
            del data[key_list[0]]
            return value
        else:
            return delete_value_by_key_list(data[key_list[0]], key_list[1:])
    except Exception as e:
        print(str(e))


def set_value_by_key_list(data, key_list, value):
    if len(key_list) == 1:
        if not isinstance(data, Dict):
            raise TypeError("")
        data[key_list[0]] = value
    else:
        set_value_by_key_list(data[key_list[0]], key_list[1:], value)


def key_related(args, dataset):
    key_list = args.key.split(".")
    if args.value_set:
        value_set = set()
        for data in dataset:
            value_set.add(get_value_by_key_list(data, key_list))
        pprint(value_set)
    elif args.new_key:
        new_key_list = args.new_key.split(".")
        for data in dataset:
            value = delete_value_by_key_list(data, key_list)
            set_value_by_key_list(data, new_key_list, value)


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
    elif args.key:
        dataset = [json.loads(line) for line in f.readlines()]
        key_related(args, dataset)

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
    elif args.key:
        key_related(args, dataset)

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
