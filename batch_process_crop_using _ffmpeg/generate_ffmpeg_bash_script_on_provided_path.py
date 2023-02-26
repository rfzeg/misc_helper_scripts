#!/usr/bin/env python3

"""
This script takes a path as an argument, searches for all .mp4 files within that path and its subdirectories, 
saves the file locations to a list, and then generates a ffmpeg command for each of these files.
The generated commands are saved to an external bash script file.

Usage example, search all files in the current directroy and all its subdirectories :
python3 generate_ffmpeg_bash_script_on_provided_path.py .

Author: Roberto Zegers
Date: February 2023

"""

import os
import sys

# Get the path argument from the command line
if len(sys.argv) != 2:
    print("You have to provide a path, like this: python3 build_ffmpeg_commands.py path_to_file(s)")
    sys.exit(1)
path = sys.argv[1]

# variable to define where the ffmpeg binary is located
# to determine where the binary ffmpeg command is stored execute whereis ffmpeg
ffmpeg_executable = "/usr/bin/ffmpeg"

# Create an empty list to store the file locations
mp4_files = []

# Search for .mp4 files within the path and its subdirectories
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".mp4"):
            mp4_files.append(os.path.join(root, file))

# Print out the file locations
print("Found these files:\n")
for file in mp4_files:
    print(file)

# Ask the user whether to continue or exit the program
while True:
    print("\nExemplary command: ffmpeg -i 'input_file.mp4' -filter:v \"crop=852:720:0:0\" -c:a copy 'output_file.mp4'\n")
    user_input = input("Enter 'y' to continue and see all commands generated or 'n' to exit. Continue (y/n)?:\n ")
    if user_input.lower() == "y":
        break
    elif user_input.lower() == "n":
        print("Closing.")
        sys.exit()
    else:
        print("Invalid input. Please enter 'y' to continue or 'n' to exit.")

list_of_ffmpeg_commands = []
for path_to_file in mp4_files:
    # Build this command:
    # ffmpeg -i 'input_file.mp4' -filter:v "crop=852:720:0:0" -c:a copy 'output_file.mp4' 

    command_as_list = [
        ffmpeg_executable,
        "-i",
        "\""+path_to_file+"\"",
        "-filter:v",
        "\"crop=852:720:0:0\"",
        "-c:a copy",
        "\""+path_to_file[:-9]+"_852x720.mp4"+"\""
        ]
    list_of_ffmpeg_commands.append(command_as_list)

# print for debugging
for command in list_of_ffmpeg_commands:
    print(*command)
print("\n")

# Ask the user whether to continue or exit the program
while True:
    user_input = input("Enter 'y' to continue and write the commands to the file 'run_ffmpeg_on_generated_commands.sh'. Continue (y/n)?: ")
    if user_input.lower() == "y":
        break
    elif user_input.lower() == "n":
        print("Closing.")
        sys.exit()
    else:
        print("Invalid input. Please enter 'y' to continue or 'n' to exit.")

# Write the commands to bash script file
with open('run_ffmpeg_on_generated_commands.sh', 'w') as f:
    f.write('#!/bin/sh'+ '\n')
    for command in list_of_ffmpeg_commands:
        f.write(' '.join(command) + '\n')

print("\nYou can now execute the generated bash script like so: ./run_ffmpeg_on_generated_commands.sh\n")
