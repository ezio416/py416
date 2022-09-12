'''
Name:    py416.filesystem
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-09-12

Functions for file system manipulation
'''
from datetime import datetime as dt
import os
import shutil as sh
import sys

from .general import gettype, timestamp, unpack

class File():
    def __init__(self, path):
        self.path = realpath(path)
        self.isdir = os.path.isdir(self.path)
        self.ctime = os.path.getctime(self.path)
        self.ctimes = dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')

    def __repr__(self):
        return f'py416.filesystem.File(\'{self.path}\')'

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
    def isroot(self) -> bool:
        return self.path == str(self.parent)

    @property
    def mtime(self) -> float:
        return os.path.getmtime(self.path)

    @property
    def mtimes(self) -> list:
        return dt.fromtimestamp(self.mtime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')

    @property
    def name(self) -> str:
        return os.path.basename(self.path) if not self.isroot else self.path

    @property
    def parent(self) -> str:
        return File(parent(self.path))

    @property
    def parts(self) -> list:
        return splitpath(self.path)

    @property
    def root(self) -> str:
        return self.parts[0]

    @property
    def size(self) -> int:
        return os.path.getsize(self.path)

    @property
    def stem(self) -> str:
        return self.name if self.isdir else self.name.split('.')[0]

    @property
    def suffix(self) -> str:
        return '.' + self.name.split('.')[-1] if not self.isdir else ''

    def delete(self, force:bool=False):
        '''
        - Deletes file/directory
        - If the object is a directory and all subdirs are empty, recursively deletes them
        - Input: `force` (`bool`): whether to force deletion via `shutil.rmtree()`
        '''
        force = bool(force)
        if self.exists:
            if self.isdir:
                if force:
                    sh.rmtree(self.path)
                else:
                    rmdir(self.path)
            else:
                os.remove(self.path)
        return self

    def move(self, dest:str):
        '''
        - Moves file
        - Input: `dest` (`str`): directory to move file into
        '''
        self.path = move(self.path, dest)
        return self

    def rename(self, new_name:str):
        '''
        - Renames file, keeping in same directory
        - Input: `new_name` (`str`): new file name
        '''
        self.path = rename(self.path, new_name)
        return self

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

def checkzip(path:str) -> bool:
    '''
    - Imports: `py7zr`: `path` ends with .7z
    - Checks if an archive file (.7z or .zip) exists and is valid
    - Deletes if invalid or incomplete
    - Input: `path` (`str`): path to the archive file
    - Return:
        - `True`: file exists and is valid
        - `False`: file doesn't exist, possibly because we deleted it due to corruption
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    try:
        if path.endswith('.7z'):
            from py7zr import exceptions, SevenZipFile
            try:
                with SevenZipFile(path, 'r') as z:
                    pass
                return True
            except exceptions.Bad7zFile:
                os.remove(path)
                return False
        elif path.endswith('.zip'):
            from zipfile import BadZipFile, ZipFile
            try:
                with ZipFile(path) as z:
                    pass
                return True
            except BadZipFile:
                os.remove(path)
                return False
    except FileNotFoundError:
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
    if gettype(path) != gettype(msg) != 'str':
        raise ValueError('Input must be a string')
    if gettype(ts_args) not in ['list', 'tuple']:
        raise ValueError('Input must be a list/tuple')
    ts = bool(ts)
    makedirs(parent(path))
    now = timestamp(*ts_args) + '  ' if ts else ''
    orig_stdout = sys.stdout
    try:
        with open(path, 'a') as file:
            sys.stdout = file
            print(f'{now}{msg}')
    except Exception:
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
    dirname = lambda path_: realpath(f'{realpath(path_)}/..')
    if getattr(sys, 'frozen', False):
        return dirname(sys.executable)
    try:
        return dirname(path)
    except NameError:
        return getcwd()

def pathjoin(*parts) -> str:
    '''
    - Imitator for `os.path.join()`
    - Joins parts of a path into a string path
    - Input: `parts` (iterable): directories/file to join together
    - Return: `str` with path (formatted with `/`)
    '''
    parts_ = [str(item).replace('/', '').replace('\\', '') for item in unpack(parts)]
    return '/' if parts_ == [''] else '/'.join(parts_)

def realpath(path:str) -> str:
    '''
    - Wrapper for `os.path.realpath()`
    - Gets the path of something
    - Input: `filedir` (`str`): file or directory
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    return(forslash(os.path.realpath(path)))

def rename(path:str, name:str) -> str:
    '''
    - Wrapper for `os.rename()`
    - Renames file without moving it
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

def rmdir(path:str, delroot:bool=True) -> int:
    '''
    - Wrapper for `os.rmdir()`
    - Recursively deletes empty directories
    - Input:
        - `dirpath` (`str`): directory path to delete within
        - `delroot` (`bool`): whether to delete `dirpath` as well
    - Return: number of deleted directories
    '''
    count = 0
    if not os.path.isdir(path):
        return 0
    files = listdir(path)
    if len(files):
        for item in files:
            if os.path.isdir(item):
                count += rmdir(item)
    files = os.listdir(path)
    if not len(files) and delroot:
        os.rmdir(path)
        count += 1
    return count

def splitpath(path:str) -> list:
    '''
    - Splits a path string into its parts
    - Input: `path` (`str`): path
    - Return: `list` of directories/file
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    result = forslash(path).split('/')
    result[0] = f'{result[0]}/' # root
    if result[1] == '':
        return [result[0]]
    return result

def unzip(path:str, delete:bool=False) -> int:
    '''
    - Unzips archive files of type: (.7z, .gz, .rar, .tar, .zip)
    - Input:
        - `path` (`str`): path to archive file
        - `delete` (`bool`): whether to delete archive after unzipping
            - Default: `False`
    - Return:
        - `0` for success
        - `1` for delete failure
        - `2` for unzip failure
        - `-1` if nothing was attempted
    '''
    if gettype(path) != 'str':
        raise TypeError('Input must be a string')
    delete = bool(delete)
    fparent = parent(path)
    if path.endswith('.7z'):
        try:
            from py7zr import unpack_7zarchive
            unpack_7zarchive(path, fparent)
            if delete:
                os.remove(path)
        except Exception:
            return 2
    elif path.endswith(tuple(['.gz', '.rar', '.tar', '.zip'])):
        try:
            sh.unpack_archive(path, fparent)
            if delete:
                os.remove(path)
        except Exception:
            return 2
    else:
        return -1
    return 0

def unzipdir(dir:str='.') -> int:
    '''
    - Unzips all archives in a directory until it is unable to continue
    - Input: `dir` (`str`): directory from which to unzip archives
        - Default: current working directory
    - Return: `int` of unzipped archives
    '''
    unzipped = 0
    while True:
        unzipped_thisrun = 0
        for file in listdir(dir, dirs=False):
            if not unzip(file, delete=True):
                unzipped += 1
                unzipped_thisrun += 1
        if not unzipped_thisrun:
            break
    return unzipped

