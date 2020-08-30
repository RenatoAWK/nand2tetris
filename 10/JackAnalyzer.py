#!/usr/bin/env python3
import sys, os, re

FILE_REGEX = re.compile(r"""(.)+\.jack""")
DIRECTORY_REGEX = re.compile(r"""[\w]*/*""")


def is_file(arg_content):
    return bool(FILE_REGEX.match(arg_content))


def is_directory(arg_content):
    return bool(DIRECTORY_REGEX.match(arg_content))


def load_files(arg_content):
    files_names = []
    files = []
    if is_file(arg_content):
        files_names.append(os.path.abspath(arg_content))
    elif is_directory(arg_content):
        my_directory_content = os.listdir(f'{os.path.abspath(arg_content)}/')
        for file_name in my_directory_content:
            if is_file(file_name):
                files_names.append(os.path.abspath(f'{arg_content}/{file_name}'))
    else:
        raise Exception('Error: Console input invalid for jack file or directory')

    for file_name in files_names:
        file = open(file_name, 'r')
        file_strings = file.readlines()
        file.close()
        files.append(file_strings)

    return files


def debug_mode():
    """debug mode"""
    test = ['JackAnalyzer.py', 'teste/outro-teste/']
    if len(test) == 2:
        files = load_files(test[1])
        print(files)
    else:
        raise Exception('Error: Missing input')


if __name__ == '__main__':
    debug = True
    if len(sys.argv) == 2:
        files = load_files(sys.argv[1])
        print(files)
    else:
        if debug:
            debug_mode()
        else:
            raise Exception('Error: Missing input')

