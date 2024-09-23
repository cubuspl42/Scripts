#!/usr/bin/env python3

import argparse
import subprocess

def git_upstream_diff(path, branch, fetch):
    if fetch:
        # Fetch the latest changes from the upstream
        subprocess.run(['git', 'fetch', branch.split('/')[0]], check=True)

    # Find the commit hash of the last common ancestor
    result = subprocess.run(['git', 'merge-base', 'HEAD', branch], 
                            check=True, stdout=subprocess.PIPE)
    commit_hash = result.stdout.decode().strip()

    # Get the changes in the file since that commit
    subprocess.run(['git', 'diff', f'{commit_hash}:{path}', f'{branch}:{path}'], check=True)

def main():
    # Create the parser
    parser = argparse.ArgumentParser(prog='git_upstream_diff', 
                                     description='Get changes in a file since the last merge with a specific branch.')

    # Add the arguments
    parser.add_argument('Path', metavar='path', type=str, help='the path to the file')
    parser.add_argument('--fetch', action='store_true', help='fetch the latest changes from the upstream')
    parser.add_argument('--branch', metavar='branch', type=str, default='upstream/main', help='the branch to compare with')

    # Parse the arguments
    args = parser.parse_args()

    git_upstream_diff(args.Path, branch=args.branch, fetch=args.fetch)

if __name__ == "__main__":
    main()
