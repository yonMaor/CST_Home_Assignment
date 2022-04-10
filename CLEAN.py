import clean_command

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-p', '--path', help='Path to the folder')
parser.add_argument('-f', '--folder', help='Folder name')

args = parser.parse_args()

clean = clean_command.CleanCommand(args.path, args.folder)

file_dict = clean.clean_dir()
