'''
Name:    py416.filesystem
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-08-18

Methods for file system manipulation
'''
import os
import sys

from .general import get_iterable_items, get_type

def cd(dir:str='..') -> bool:
    '''
    - Wrapper for `os.chdir`
    - Changes current working directory
    - Input:
        - `dir`: `str` with path
            - Default: up a directory
    - Return:
        - `True`: success
        - `False`: error
    '''
    if get_type(dir) != 'str':
        raise TypeError('Input must be a string')
    try:
        os.chdir(dir)
        return True
    except Exception:
        return False

def forslash(path:str) -> str:
    '''
    - Replaces `\\` in paths with `/`
    - Used to unify path formatting between OS types
    - Input:
        - `path`: `str` with path
    - Return:
        - `str` with path separated by `/`
    '''
    return path.replace('\\', '/')

def getcwd() -> str:
    '''
    - Wrapper for `os.getcwd`
    - Gets the current working directory
    - Return:
        - `str` with path separated by `/`
    '''
    return(forslash(os.getcwd()))

def listdir(dir_parent:str='', dirs:bool=True, files:bool=True) -> list[str]:
    '''
    - Wrapper for `os.listdir`
    - Lists directories/files within a directory
    - Input:
        - `dir_parent`: `str` with path of directory to search in
            - Default: current working directory
        - `dirs`: set `True` to list directories
            - Default: `True`
        - `files`: set `True` to list files
            - Default: `True`
    - Return:
        - `list` of `str` with paths separated by `/`
    '''
    if get_type(dir_parent) != 'str':
        raise TypeError('Input must be a string')
    result = []
    if not dir_parent:
        dir_parent = getcwd()
    for child in os.listdir(dir_parent):
        child = f'{dir_parent}/{child}'
        if all(dirs, os.path.isdir(child)):
            result.append(child)
        if all(files, not os.path.isdir(child)):
            result.append(child)
    return result

def makedirs(*dirs) -> list[str]:
    '''
    - Wrapper for `os.makedirs`
    - Creates directories if nonexistent
    - Input:
        - `dirs`:
            - `str` directory path
            - Nestings of `list`/`tuple` objects with `str` directory path base elements
    - Return:
        - `list` of `str` of created directories separated by `/`
    '''
    if get_type(dirs) not in ['list', 'str', 'tuple']:
        raise TypeError('Input must be a string, list, or tuple')
    created = []
    for dir in get_iterable_items(dirs):
        dir = forslash(dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
            created.append(dir)
    return created

def parent(path:str='') -> str:
    '''
    - Gets the directory containing something
    - Input:
        - `path`: `str` with path
            - Default: file that called `parent()`
    - Return:
        - `str` with path separated by `/`
            - Directory containing `path`
            - Directory containing file that called `parent()`
    '''
    if get_type(path) != 'str':
        raise TypeError('Input must be a string')
    dirname = lambda path_: forslash(os.path.dirname(path_))
    if path:
        return dirname(path)
    if getattr(sys, 'frozen', False):
        return dirname(sys.executable)
    try:
        return dirname(realpath(__file__))
    except NameError:
        return getcwd()

def realpath(filedir:str) -> str:
    '''
    - Wrapper for `os.path.realpath`
    - Gets the path of something
    - Input:
        - `filedir`: `str` with file or directory
    - Return:
        - `str` with path separated by `/`
    '''
    return(forslash(os.path.realpath(filedir)))

def splitpath(path:str) -> list:
    '''
    - Splits a path string
    - Input:
        - `path`: `str` with path
    - Return:
        - `list` of directories/file
    '''
    return forslash(path).split('/')

