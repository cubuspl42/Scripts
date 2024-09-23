#!/bin/bash

# Set the remote name and branch prefix
remote="origin"
prefix="dependabot/"

# Get the list of branches
branches=$(git branch -r | grep "$remote/$prefix")

# Loop over branches
for branch in $branches
do
    echo "Processing $branch"
    # Cherry-pick the commits from this branch
    git cherry-pick $branch
done
