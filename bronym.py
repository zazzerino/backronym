import linecache
import os
import random
import sys


wordfile = '/usr/share/dict/words'


def handle_usage_err(argv, wordfile):
    # Does the file exist?
    if not os.path.isfile(wordfile):
        sys.exit(f'Could not find word file at {wordfile}.')

    # Did the user give a commandline argument when calling the script?
    arg_count = len(argv)
    if arg_count != 2:
        sys.exit(f'Expected one argument but received {arg_count-1}.')


def increment_char(char):
    '''Returns the next character in the ascii table.'''
    return chr(ord(char)+1)


def find_char_offsets(filename):
    '''Returns a dict where each key is a letter of the alphabet and each
    value is the line number where words beginning with that letter start.'''
    offsets = {}
    char = 'a'
    with open(filename, 'r', encoding='utf-8') as f:
        for i, word in enumerate(f):
            if word.lower().startswith(char):
                offsets[char] = i
                if char == 'z':
                    break
                else:
                    char = increment_char(char)
    return offsets


def count_lines(filepath):
    linecount = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for i in f:
            linecount += 1
    return linecount


def rand_word(filename, char, offsets):
    start = offsets[char]

    if char != 'z':
        end = offsets[increment_char(char)]
    else:
        end = count_lines(filename)

    rand_index = random.randint(start, end)
    return linecache.getline(filename, rand_index).rstrip()


def gen_backronym(wordfile, word):
    chars = list(word)
    offsets = find_char_offsets(wordfile)

    words = []
    for char in chars:
        words.append(rand_word(wordfile, char, offsets))

    return ' '.join(words)


if __name__ == '__main__':
    handle_usage_err(sys.argv, wordfile)
