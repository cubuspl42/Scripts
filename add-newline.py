#!/usr/bin/env python3

import os
import re
import argparse

def add_trailing_newline(file_path):
    with open(file_path, 'r+') as file:
        content = file.read()
        if not content.endswith('\n'):
            file.write('\n')

def main():
    parser = argparse.ArgumentParser(description='Add trailing newline to files matching a regex.')
    parser.add_argument('regex', type=str, help='The regex pattern to match file names.')

    args = parser.parse_args()
    pattern = re.compile(args.regex)

    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if pattern.match(file):
                add_trailing_newline(os.path.join(root, file))

if __name__ == "__main__":
    main()
