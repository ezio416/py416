'''
Name:    py416.filesystem
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-09-07

Methods for file system manipulation
'''
from datetime import datetime as dt
import os
import shutil as sh
import sys

from .general import gettype, timestamp, unpack

class File():
    def __init__(self, path):
        self.path = forslash(path)
        self.isdir = os.path.isdir(self.path)
        self.ctime = os.path.getctime(self.path)
        self.ctimes = dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')
    
    def __repr__(self):
        return 'py416.filesystem.File()'
    
    def __str__(self):
        return self.path
    
    @property
    def atime(self) -> float:
        return os.path.getatime(self.path)

    @property
    def atimes(self) -> list:
        return dt.fromtimestamp(self.atime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')
    
    @property
    def children(self) -> list:
        return listdir(self.path) if self.isdir else []
        
    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @property
    def mtime(self) -> float:
        return os.path.getmtime(self.path)
    
    @property
    def mtimes(self) -> list:
        return dt.fromtimestamp(self.mtime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')
    
    @property
    def name(self) -> str:
        return os.path.basename(self.path)
    
    @property
    def parent(self) -> str:
        return File('/'.join(self.path.split('/')[:-1]))
    
    @property
    def parts(self) -> list:
        return self.path.split('/')
    
    @property
    def size(self) -> int:
        return os.path.getsize(self.path)
    
    @property
    def stem(self) -> str:
        return self.name.split('.')[0]
    
    @property
    def suffix(self) -> str:
        return '.' + self.name.split('.')[-1] if not self.isdir else ''
    
    def delete(self):
        '''
        - Deletes file
        '''
        if self.exists:
            os.remove(self.path)

    def move(self, dest:str):
        '''
        - Moves file
        - Input: `dest` (`str`): directory to move file into
        '''
        self.path = move(self.path, dest)

    def rename(self, new_name:str):
        '''
        - Renames file, keeping in same directory
        - Input: `new_name` (`str`): new file name
        '''
        self.path = rename(self.path, new_name)

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
    - Return: `str` with path (formatted with `/`)
    '''
    return path.replace('\\', '/')

def getcwd() -> str:
    '''
    - Wrapper for `os.getcwd()`
    - Gets the current working directory
    - Return: `str` with path (formatted with `/`)
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
    - Return: `list` of `str` with paths (formatted with `/`)
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
    try:
        with open(path, 'a') as file:
            sys.stdout = file
            print(f'{now}{msg}')
    except Exception as e:
        pass
    finally:
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

def move(path:str, dest:str) -> str:
    '''
    - Wrapper for `shutil.move()`
    - Moves file with some extra safety
    - Input:
        - `path` (`str`): path to file/directory
        - `dest` (`str`): path to destination directory
    - Return: `str` with path to destination file (formatted with `/`)
    '''
    if not os.path.exists(path):
        raise FileNotFoundError('The file does not exist')
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise FileExistsError('The destination exists as a file')
    makedirs(dest)
    if os.path.exists(f'{dest}/{os.path.basename(path)}'):
        raise FileExistsError('The destination file already exists')
    return forslash(sh.move(path, dest))

def parent(path:str) -> str:
    '''
    - Gets the directory containing something
    - Input: `path` (`str`): path to find the parent of
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    dirname = lambda path_: forslash(os.path.dirname(path_))
    if getattr(sys, 'frozen', False):
        return dirname(sys.executable)
    try:
        return dirname(realpath(path))
    except NameError:
        return getcwd()

def realpath(filedir:str) -> str:
    '''
    - Wrapper for `os.path.realpath()`
    - Gets the path of something
    - Input: `filedir` (`str`): file or directory
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(filedir) != 'str':
        raise TypeError('Input must be a string')
    return(forslash(os.path.realpath(filedir)))

def rename(path:str, name:str) -> str:
    '''
    - Wrapper for `os.rename()`
    - Renames file
    - Input:
        - `path` (`str`): path to file/directory to be renamed
        - `name` (`str`): new basename for file (not path)
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != gettype(name) != 'str':
        raise TypeError('Input must be a string')
    new_path = f'{parent(path)}/{name}'
    os.rename(path, new_path)
    return new_path

def rmdir(dirpath:str, delroot:bool=True) -> int:
    '''
    - Wrapper for `os.rmdir()`
    - Recursively deletes empty directories
    - Input:
        - `dirpath` (`str`): directory path to delete within
        - `delroot` (`bool`): whether to delete `dirpath` as well
    - Return: number of deleted directories
    '''
    count = 0
    if not os.path.isdir(dirpath):
        return 0
    files = listdir(dirpath)
    if len(files):
        for item in files:
            if os.path.isdir(item):
                count += rmdir(item)
    files = os.listdir(dirpath)
    if not len(files) and delroot:
        os.rmdir(dirpath)
        count += 1
    return count

def splitpath(path:str) -> list:
    '''
    - Splits a path string
    - Input: `path` (`str`): path
    - Return: `list` of directories/file
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    return forslash(path).split('/')

