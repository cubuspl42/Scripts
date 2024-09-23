#!/usr/bin/env python3

import subprocess
import sys
from urllib.parse import urlparse, unquote

def run(cmd):
    print(f"Running command: {' '.join(cmd)}")
    confirm = input("Press Enter to continue or any other key to abort: ")
    if confirm == '':
        subprocess.run(cmd, check=True)
    else:
        print("Command aborted.")
        sys.exit(1)

def parse_github_url(url):
    # Parse the URL
    parsed_url = urlparse(unquote(url))
    path_parts = parsed_url.path.split('/')
    
    if len(path_parts) < 5 or path_parts[3] != 'tree':
        print("Invalid GitHub branch URL.")
        sys.exit(1)

    user = path_parts[1]
    repo = path_parts[2]
    branch = '/'.join(path_parts[4:])

    return user, repo, branch

def checkout_fork_branch(url):
    user, repo, branch = parse_github_url(url)

    # Add the fork as a remote
    remote_url = f"https://github.com/{user}/{repo}.git"
    run(["git", "remote", "add", user, remote_url])

    # Fetch the data from the new remote
    run(["git", "fetch", user])

    # Checkout the specific branch
    run(["git", "checkout", "-b", branch, f"{user}/{branch}"])

if len(sys.argv) != 2:
    print("Usage: script <github url>")
else:
    checkout_fork_branch(sys.argv[1])
