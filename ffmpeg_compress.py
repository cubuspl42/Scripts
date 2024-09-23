#!/usr/bin/env python3
import sys
import os
import av
import subprocess
from os import path

def round_down_to_even(number):
    """Round down to the nearest even number."""
    return number // 2 * 2

def get_video_size(file_path):
    with av.open(file_path) as input_container:
        input_stream = next(s for s in input_container.streams if s.type == 'video')

        return (input_stream.width, input_stream.height)

def compress_video(input_file, output_directory_path):
    # Get the basename without extension
    input_basename = os.path.splitext(os.path.basename(input_file))[0]

    # Define output file
    output_file_name = f"{input_basename}-compressed.mp4"
    output_file_path = path.join(output_directory_path, output_file_name)

    (old_width, old_height) = get_video_size(input_file)

    # Calculate new resolution
    new_width = round_down_to_even(old_width // 2)
    new_height = round_down_to_even(old_height // 2)

    subprocess.run(
        ["ffmpeg", "-i", input_file, "-vf", f"scale={new_width}:{new_height}", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p", output_file_path],
        check=True
    )

def main(argv):
    # Check if the input file is provided
    if len(argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    # Get input file
    input_file = argv[1]

    compress_video(input_file, f"out")

if __name__ == "__main__":
    main(sys.argv)
