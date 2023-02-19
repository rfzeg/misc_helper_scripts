"""
Python script to help automate the task of 
splitting a video file into smaller parts.
"""

# module required to run shell commands from Python
import subprocess
import csv

# Load the CSV file into a list of dictionaries
entries = []
with open("example_semicolon.csv", "r") as file:
    # the delimiter parameter is set to ; to read the values separated by semicolons
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        entries.append(row)

# variable to define where the ffmpeg binary is located
# to determine where the binary ffmpeg command is stored execute whereis ffmpeg
ffmpeg_executable = "/usr/bin/ffmpeg"

# Cut a video using the start and end time of the video by using the following command: 
# ffmpeg -i "in.mp4" -ss 00:00:08 -to 00:00:37 -c copy -avoid_negative_ts make_zero "out.mp4"
# -c is short for -codec
# -c copy means set all codec operations to copy (without doing a slow re-encode)
# this shifts the timestamp of the video to 0 to avoid the black screen at the beginning

# Loop over the list of dictionaries and print its content
video_segments = []
for entry in entries:

    command_as_list = [
        ffmpeg_executable,
        "-i",
        entry["input_file"],
        "-ss",
        entry["start_time"],
        "-to",
        entry["end_time"],
        "-c copy",
        "-avoid_negative_ts make_zero",
        entry["output_file"]
        ]
    video_segments.append(command_as_list)

# print for debugging
for command in video_segments:
    print(*command)




