'''
| Author:  Ezio416
| Created: 2023-03-14
| Updated: 2024-01-31

- Functions behind console scripts
- Call these functions directly by name from the command line
'''
import sys

from .files import rmdir, unzipdir
from .json import pretty


# def jsp():
#     '''
#     - takes one or more .json files and makes them human-readable
#     - will only work on files ending with .json, all other files are ignored

#     Flags
#     ---------
#     - -p, --path (str): path to file/folder (default current working directory)
#         - if a file, will only do that file
#         - if a folder, will do every file in that folder
#     - -i, --indent (int): number of spaces to indent by (default 4)
#     - -b, --sort_keys (bool): whether to sort keys (default True)
#     '''
#     if len(sys.argv) > 1:
#         args: list = sys.argv
#         args_default: list = ['', 4, True]

#         if args in ('-p', '--path'):
#             if len(args)

#         print(f'formatted {pretty(*args_default)} .json files')
#         return

#     print(f'formatted {pretty()} .json files')


def rmd():
    '''
    - recursively deletes empty directories
    - wraps `os.rmdir() <https://docs.python.org/3/library/os.html#os.rmdir>`_

    Arguments
    ---------
    - none: delete empty folders where we are, but leave our parent intact
    - one argument: path to folder
        - folder in which to delete empty folders
    - two arguments: path to folder, anything
        - if a second value is present, we'll also try to delete the given folder
        - the second value itself is ignored
    '''
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print(f'deleted {rmdir(sys.argv[1])} empty folders')
            return
        print(f'deleted {rmdir(sys.argv[1], delroot=False)} empty folders')
        return
    print(f'deleted {rmdir(".", delroot=False)} empty folders')


def uzd():
    '''
    - unzips all archive files in a folder until it is unable to continue
    - recursive on archive files, but not folders
    - deletes all archive files as it unzips
    - supports archive files of type: (.7z, .gz, .rar, .tar, .zip)

    Arguments
    ---------
    - if any argument is passed, the script will stop upon error
    '''
    if len(sys.argv) > 1:
        print(f'unzipped {unzipdir(ignore_errors=False)} archive file(s)')
        return
    print(f'unzipped {unzipdir()} archive file(s)')
