#!/usr/bin/env python3

import argparse
from stl import mesh
import numpy as np

def process_stl(input_file, output_file, tolerance):
    # Load the STL files
    your_mesh = mesh.Mesh.from_file(input_file)

    # Get all unique z values and sort them
    unique_z = np.unique(your_mesh.vectors[:,:,2])
    unique_z.sort()

    # Group close values into buckets
    buckets = np.split(unique_z, np.where(np.diff(unique_z) > tolerance)[0] + 1)

    # Calculate averages for each bucket and create a mapping from old to new z values
    z_mapping = {value: np.mean(bucket) for bucket in buckets for value in bucket}

    # Replace z values based on the mapping
    z_values = your_mesh.vectors[:,:,2]
    your_mesh.vectors[:,:,2] = np.vectorize(z_mapping.get)(z_values)

    # Save the modified mesh
    your_mesh.save(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process STL files to average z-values within a tolerance.')
    parser.add_argument('input_file', type=str, help='The input STL file to process.')
    parser.add_argument('output_file', type=str, help='The output file to save the processed STL.')
    parser.add_argument('--tolerance', type=float, default=0.01, help='The tolerance for z-value averaging.')

    args = parser.parse_args()

    process_stl(args.input_file, args.output_file, args.tolerance)
