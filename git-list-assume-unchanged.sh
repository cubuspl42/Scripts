#!/bin/bash

# List all files marked as --assume-unchanged
git ls-files -v | grep '^[[:lower:]]'
