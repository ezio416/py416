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


def jsp():
    '''
    - takes one or more .json files and makes them human-readable
    - will only work on files ending with .json, all other files are ignored
    - pass arguments directly after their corresponding flags, i.e. "-p path/to/file -i 2 -s False -o False"

    Flags
    ---------
    - -p (str): path to file/folder (default current working directory)
        - if a file, will only do that file
        - if a folder, will do every file in that folder
    - -i (int): number of spaces to indent by (default 4)
    - -s (bool): whether to sort keys (default True)
    - -o (bool): whether to overwrite an existing '_pretty.json' file (default True)
    '''
    if len(sys.argv) > 1:
        args_given: list[str] = sys.argv[1:]
        args_to_pass: list = ['.', 4, True, True]

        while True:
            if len(args_given) == 0:
                break

            if args_given[0] == '-p':
                if len(args_given) < 2:
                    print('path flag passed but no path given!')
                    return

                if args_given[1] in ('-i', '-s', '-o'):
                    print(f'invalid arguments: {args_given}')
                    return

                args_to_pass[0] = args_given[1]

            elif args_given[0] == '-i':
                if len(args_given) < 2:
                    print('indent flag passed but no indent value given!')
                    return

                if args_given[1] in ('-p', '-s', '-o'):
                    print(f'invalid arguments: {args_given}')
                    return

                try:
                    indent: int = int(args_given[1])
                except Exception as e:
                    print(f'error with indent value: {e}')
                    return

                if indent < 0:
                    print('given indent value is negative, setting to 0')
                    indent = 0

                args_to_pass[1] = indent

            elif args_given[0] == '-s':
                if len(args_given) < 2:
                    print('sort flag passed but no sort value given!')
                    return

                if args_given[1] in ('-p', '-i', '-o'):
                    print(f'invalid arguments: {args_given}')
                    return

                args_to_pass[2] = bool(args_given[1])

            elif args_given[0] == '-o':
                if len(args_given) < 2:
                    print('overwrite flag passed but no overwrite value given!')
                    return

                if args_given[1] in ('-p', '-i', '-s'):
                    print(f'invalid arguments: {args_given}')
                    return

                args_to_pass[3] = args_given[1]

            else:
                print(f'invalid arguments given: {args_given}')
                return

            args_given.pop(0)
            args_given.pop(0)

        print(f'formatted {pretty(*args_to_pass)} .json files')
        return

    print(f'formatted {pretty()} .json files')


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
