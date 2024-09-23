#!/usr/bin/env python3
import os
import subprocess
import argparse
import av
import shutil
import tempfile

compression_bps_ratio_threshold = 700_000 # 700 kB/s

def compress_video(file_path):
    # Move original to temp directory and print the temp path
    temp_dir = tempfile.mkdtemp()
    tmp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
    shutil.move(file_path, tmp_file_path)
    
    print(f"Moved original file to temporary path: {tmp_file_path}")
    
    # Ensure the output file always has a .mp4 extension
    output_file_path = os.path.splitext(file_path)[0] + ".mp4"
    
    subprocess.run(
        ["ffmpeg", "-i", tmp_file_path, "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p", output_file_path],
        check=True
    )

def compress_all_videos(source_directory_path):
    for file_name in os.listdir(source_directory_path):
        name_without_extension, extension = os.path.splitext(file_name)
        extension = extension.lower()

        # Ignore non-video files
        if extension not in [".mp4", ".mov"]:
            continue

        file_path = os.path.join(source_directory_path, file_name)

        # Ignore already compressed files
        if is_compressed(file_path):
            continue

        compress_video(file_path)

def is_compressed(file_path):
    bps_ratio = compute_bytes_per_second_ratio(file_path)

    print(file_path, bps_ratio)

    # Assume that if the size per second is below this threshold, the video is compressed
    return bps_ratio < compression_bps_ratio_threshold

def compute_bytes_per_second_ratio(file_path):
    container = av.open(file_path)
    video_stream = next(s for s in container.streams if s.type == 'video')
    duration = video_stream.duration * video_stream.time_base
    size = os.path.getsize(file_path)

    return float(size / duration)

def main():
    parser = argparse.ArgumentParser(description="Compress all video files in a directory.")
    parser.add_argument("source_directory", help="The directory containing the video files to compress.")

    args = parser.parse_args()

    compress_all_videos(args.source_directory)

if __name__ == "__main__":
    main()
