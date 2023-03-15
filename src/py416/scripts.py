'''
| Author:  Ezio416
| Created: 2023-03-14
| Updated: 2023-03-14

- Functions behind console scripts
- Call these functions directly by name from the command line
'''
import sys

from .files import rmdir, unzipdir


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
