#!/usr/bin/env python3
import os
import sys
import subprocess
from os import path
import ffmpeg
from threading import Thread
import os

screengrabs_path = path.expanduser('~/Desktop/Screengrabs')
screengrabs_out_path = path.join(screengrabs_path, 'out')

def convert_to_mp4(input_file_path, output_directory_path):
    base_name = path.splitext(path.basename(input_file_path))[0]
    output_file_path = path.join(output_directory_path, f'{base_name}-converted.mp4')

    print("output_directory_path=", output_directory_path)

    print("output_file_path=", output_file_path)

    # Run the ffmpeg command with the input file and output file
    try:
        (
            ffmpeg
            .input(input_file_path)
            .output(output_file_path, an=None)
            .run(overwrite_output=True)
        )

        print(f'Conversion complete')
    except ffmpeg.Error as e:
        print('Error occurred during conversion: ' + str(e))
        sys.exit(1)

def round_down_to_even(number):
    """Round down to the nearest even number."""
    return number // 2 * 2

def get_video_size(file_path):
    probe = ffmpeg.probe(file_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return (video_stream['width'], video_stream['height'])

def compress_video(input_file_path, output_directory_path):
    # Get the basename without extension
    input_basename = os.path.splitext(os.path.basename(input_file_path))[0]

    # Define output file
    output_file_name = f"{input_basename}-compressed.mp4"
    output_file_path = path.join(output_directory_path, output_file_name)

    (old_width, old_height) = get_video_size(input_file_path)

    # Calculate new resolution
    new_width = round_down_to_even(old_width // 2)
    new_height = round_down_to_even(old_height // 2)

    (
        ffmpeg
            .input(input_file_path)
            .output(output_file_path, vf=f'scale={new_width}:{new_height}', preset='slow', crf=23, pix_fmt='yuv420p', **{'c:v': 'libx264'})
            .run(overwrite_output=True)
    )

def adb_pull(file_name, output_dir):
    subprocess.run(['adb', 'pull', file_name, output_dir])

def main(argv):
    print("Start")

    if len(argv) < 2:
        print("Usage: python script.py <prefix>")
        sys.exit(1)
    
    prefix = argv[1]
    
    adb_pull(f'/sdcard/Movies/{prefix}-android.mp4', screengrabs_path)
    adb_pull(f'/sdcard/Movies/{prefix}-android-web.mp4', screengrabs_path)

    # Run in parallel
    threads = [
        Thread(target=convert_to_mp4, args=(path.join(screengrabs_path, f'{prefix}-web.mov'), screengrabs_out_path)),
        Thread(target=convert_to_mp4, args=(path.join(screengrabs_path, f'{prefix}-desktop.mov'), screengrabs_out_path)),
        Thread(target=compress_video, args=(path.join(screengrabs_path, f'{prefix}-ios.mov'), screengrabs_out_path)),
        Thread(target=compress_video, args=(path.join(screengrabs_path, f'{prefix}-ios-web.mov'), screengrabs_out_path)),
        Thread(target=compress_video, args=(path.join(screengrabs_path, f'{prefix}-android.mp4'), screengrabs_out_path)),
        Thread(target=compress_video, args=(path.join(screengrabs_path, f'{prefix}-android-web.mp4'), screengrabs_out_path)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        print("Joining...")
        thread.join()

    print("Done")

if __name__ == "__main__":
    main(sys.argv)
