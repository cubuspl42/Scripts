#!/usr/bin/env python3
import os
import subprocess
import re
import datetime
import argparse

def get_video_duration(file_path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration_seconds = float(result.stdout)
    return datetime.timedelta(seconds=duration_seconds)

def sum_video_durations(directory_path):
    total_duration = datetime.timedelta()
    for file_name in os.listdir(directory_path):
        name_without_extension, extension = os.path.splitext(file_name)
        extension = extension.lower()

        # Ignore non-mp4 files
        if extension != ".mp4":
            continue

        file_path = os.path.join(directory_path, file_name)
        total_duration += get_video_duration(file_path)
    
    return total_duration

def main():
    parser = argparse.ArgumentParser(description="Sum up durations of all mp4 videos in a directory.")
    parser.add_argument("directory", help="The directory containing the video files.")

    args = parser.parse_args()

    total_duration = sum_video_durations(args.directory)
    print(f"Total duration of all mp4 videos in directory: {total_duration}")

if __name__ == "__main__":
    main()
