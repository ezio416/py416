'''
Name:    py416.filesystem
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-09-01

Methods for file system manipulation
'''
from datetime import datetime as dt
import os
import sys

from .general import gettype, timestamp, unpack

class File:
    def __init__(self, file):
        self.exists = os.path.exists(file)
        if self.exists:
            self.name = os.path.basename(file)
            self.path = realpath(file)
            self.parent = parent(self.path)
            self.size = os.path.getsize(self.path)

            self.isdir = os.path.isdir(file)
            self.children = listdir(file) if self.isdir else []
            self.extension = self.name.split('.')[-1] if not self.isdir else ''

            self.atime = os.path.getatime(self.path)
            self.atime_vals = dt.fromtimestamp(self.atime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')
            self.ctime = os.path.getctime(self.path)
            self.ctime_vals = dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')
            self.mtime = os.path.getmtime(self.path)
            self.mtime_vals = dt.fromtimestamp(self.mtime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')

    def delete(self):
        '''
        - Deletes file
        '''
        os.remove(self.path)
        self.exists = False

    def move(self, dest:str):
        '''
        - Moves file
        - Input: `dest` (`str`): directory to move file into
        '''
        dest = forslash(dest)
        new_path = f'{dest}/{self.name}'
        makedirs(dest)
        os.rename(self.path, new_path)
        self.path = new_path
        self.parent = dest

    def rename(self, new_name:str):
        '''
        - Renames file, keeping in same directory
        - Input: `new_name` (`str`): new file name
        '''
        new_path = f'{self.parent}/{new_name}'
        os.rename(self.path, new_path)
        self.name = new_name
        self.path = new_path

def cd(dir:str='..') -> bool:
    '''
    - Wrapper for `os.chdir()`
    - Changes current working directory
    - Input: `dir` (`str`): directory path
        - Default: up a directory
    - Return:
        - `True`: success
        - `False`: error
    '''
    if gettype(dir) != 'str':
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
    - Input: `path` (`str`): path
    - Return: `str` with path separated by `/`
    '''
    return path.replace('\\', '/')

def getcwd() -> str:
    '''
    - Wrapper for `os.getcwd()`
    - Gets the current working directory
    - Return: `str` with path separated by `/`
    '''
    return(forslash(os.getcwd()))

def listdir(path:str='', dirs:bool=True, files:bool=True) -> list:
    '''
    - Wrapper for `os.listdir()`
    - Lists directories/files within a directory
    - Input:
        - `path` (`str`): directory path to search in
            - Default: current working directory
        - `dirs` (`bool`): whether to list directories
            - Default: `True`
        - `files` (`bool`): whether to list files
            - Default: `True`
    - Return: `list` of `str` with paths separated by `/`
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    dirs = bool(dirs)
    files = bool(files)
    result = []
    path = forslash(path) if path else getcwd()
    for child in os.listdir(path):
        child = f'{path}/{child}'
        if dirs and os.path.isdir(child):
            result.append(child)
        if files and not os.path.isdir(child):
            result.append(child)
    return result

def log(path:str, msg:str, ts:bool=True, ts_args:list=[1,0,1,1,1,0]) -> None:
    '''
    - Logs to file with current timestamp
    - Creates file and its parent directory if nonexistent
    - Input:
        - `path` (`str`): path to desired log file
        - `msg` (`str`): message to log
        - `ts` (`bool`): whether to include timestamp
            - Default: `True`
        - `ts_args` (`list`/`tuple`): arguments to pass to `py416.timestamp()`
            - Default example: [2022-08-19 13:24:54 -06:00]
    '''
    if any(gettype(path) != 'str', gettype(msg) != 'str'):
        raise ValueError('Input must be a string')
    if gettype(ts_args) not in ['list', 'tuple']:
        raise ValueError('Input must be a list/tuple')
    makedirs(parent(path))
    now = timestamp(*ts_args) + '  ' if ts else ''
    orig_stdout = sys.stdout
    with open(path, 'a') as file:
        sys.stdout = file
        print(f'{now}{msg}')
        sys.stdout = orig_stdout

def makedirs(*dirs) -> None:
    '''
    - Wrapper for `os.makedirs()`
    - Creates directories if nonexistent
    - Input: `dirs`:
        - `str` directory path
        - Nestings of `list`/`tuple` objects with `str` directory path base elements
    '''
    if gettype(dirs) not in ['list', 'str', 'tuple']:
        raise TypeError('Input must be a string, list, or tuple')
    for dir in unpack(dirs):
        if not os.path.exists(dir):
            os.makedirs(dir)

def parent(path:str='') -> str:
    '''
    - Gets the directory containing something
    - Input: `path` (`str`): path to find the parent of
        - Default: file that called `parent()`
    - Return: `str` with path separated by `/`
        - Directory containing `path`
        - Directory containing file that called `parent()`
    '''
    if gettype(path) != 'str':
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
    - Wrapper for `os.path.realpath()`
    - Gets the path of something
    - Input: `filedir` (`str`): file or directory
    - Return:
        - `str` with path separated by `/`
    '''
    if gettype(filedir) != 'str':
        raise TypeError('Input must be a string')
    return(forslash(os.path.realpath(filedir)))

def splitpath(path:str) -> list:
    '''
    - Splits a path string
    - Input: `path` (`str`): path
    - Return: `list` of directories/file
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    return forslash(path).split('/')

