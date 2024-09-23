#!/usr/bin/env python3
from svgpathtools import svg2paths
import sys

def dump_sorted_segments(svg_file):
    # Load and parse the SVG file
    paths, attributes = svg2paths(svg_file)

    # List to hold all segments
    all_segments = []

    # Extract segments from each path
    for path in paths:
        all_segments.extend(path)

    # Sort segments by start point X
    sorted_segments = sorted(all_segments, key=lambda seg: seg.start.real)

    # Print sorted segments
    for i, segment in enumerate(sorted_segments):
        print(f'Segment {i + 1}:')
        print(f'Start Point: ({segment.start.real}, {segment.start.imag})')
        print(f'End Point: ({segment.end.real}, {segment.end.imag})')
        print(segment)
        print('-' * 40)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dump_sorted_segments.py <svg_file>")
        sys.exit(1)

    svg_file = sys.argv[1]
    dump_sorted_segments(svg_file)
