import sort_command

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-p', '--path', help='Path to the parent folder')
parser.add_argument('-f', '--folder', help='Folder name')

args = parser.parse_args()

sort = sort_command.SortCommand(args.path, args.folder)

print(sort.sort_dir())
