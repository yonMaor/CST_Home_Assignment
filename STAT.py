import stat_command

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-p', '--path', help='Path to the folder')
parser.add_argument('-f', '--folder', help='Folder name')
parser.add_argument('-t', '--time_stamp', help='Time stamp for earliest log to check')

args = parser.parse_args()

stat = stat_command.StatCommand(args.path, args.folder)

file_dict = stat.dir_stat(args.time_stamp)
