#!/usr/bin/env python3
import sys, os, re
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

FILE_REGEX = re.compile(r"""(.)+\.jack""")
DIRECTORY_REGEX = re.compile(r"""[\w]*/*""")

class File:
    def __init__(self, filename, content, token: JackTokenizer = None, engine: CompilationEngine = None):
        self.filename = filename
        self.content = content
        self.token = token
        self.engine = engine



def is_file(arg_content):
    return bool(FILE_REGEX.match(arg_content))


def is_directory(arg_content):
    return bool(DIRECTORY_REGEX.match(arg_content))


def removing_comments_and_becoming_inline(lines):
    for key_line, line in enumerate(lines):
        inline_position = line.find('//')
        if inline_position >= 0:
            lines[key_line] = line[:inline_position]

    inline = ''.join(lines).replace('\n','').replace('\t','')
    while inline.find('/*') >= 0:
        begin = inline.find('/*')
        end = inline.find('*/')
        inline = f'{inline[:begin]}{inline[end+2:]}'

    return inline


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
        files.append(File(file_name, removing_comments_and_becoming_inline(file_strings)))

    return files


def start(arg_content):
    files = load_files(arg_content)
    for file in files:
        file.token = JackTokenizer(file.content)
        file.token.tokenize()
        file.engine = CompilationEngine(file.token, file.filename)
        file.engine.compile()


def debug_mode():
    """debug mode"""
    test = ['JackAnalyzer.py', 'teste3.jack']
    if len(test) == 2:
        start(test[1])
    else:
        raise Exception('Error: Missing input')


if __name__ == '__main__':
    debug = True
    if len(sys.argv) == 2:
        start(sys.argv[1])
    else:
        if debug:
            debug_mode()
        else:
            raise Exception('Error: Missing input')
