'''
| Author:  Ezio416
| Created: 2024-01-31
| Updated: 2024-01-31

- Functions for interacting with json objects
'''
import json
import os

from .files import getpath, listdir


def pretty(path: str = '.', indent: int = 4, sort_keys: bool = True, overwrite: bool = True) -> int:
    '''
    - takes one or more .json files and makes them human-readable
    - will only work on files ending with .json, all other files are skipped
    - appends '_pretty' to the end of the base filename, i.e. 'data.json' becomes 'data_pretty.json'
    - skips files already ending with '_pretty.json' - we assume those are already done

    Parameters
    ----------
    path: str
        - path to file or folder to work on
        - if a file, will only do that file
        - if a folder, will do every file in that folder
            - does not search subfolders
        - default: current working directory
    indent: int
        - number of spaces to indent by
        - default: 4
    sort_keys: bool
        - whether to sort keys
        - default: True
    overwrite: bool
        - whether to overwrite a '_pretty.json' file if it already exists
        - default: True

    Returns
    -------
    int
        - number of files that were formatted
    '''
    if path == '.':
        files: tuple[str] = tuple(getpath(f) for f in listdir(dirs=False))
    else:
        if os.path.exists(path):
            if os.path.isdir(path):
                files: tuple[str] = tuple(getpath(file) for file in listdir(path, dirs=False))
            elif os.path.isfile(path):
                files: tuple[str] = getpath(path),
        else:
            print(f'invalid path given: {path}')
            return 0

    total: int = 0

    for file in files:
        parts: list[str] = file.split('.')
        pre_ext: str = '.'.join(parts[:-1])
        ext: str = parts[-1]

        if pre_ext.endswith('_pretty') or ext != 'json':
            continue

        with open(file, 'r') as f:
            contents: dict = json.loads(f.read())

        new_file: str = pre_ext + '_pretty.json'

        if not overwrite and os.path.exists(new_file):
            continue

        with open(new_file, 'w') as f:
            json.dump(contents, f, indent=indent, sort_keys=sort_keys)

        total += 1

    return total
