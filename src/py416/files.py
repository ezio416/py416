'''
Name:    py416.files
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-09-19

Functions for file system manipulation
OS-agnostic (Windows/Unix) - Windows paths will always have forward slashes
Basically everything here takes strings, so pass strings
'''
from datetime import datetime as dt
import os
import shutil as sh
import sys

from .general import gettype, timestamp, unpack

class File():
    def __init__(self, path):
        self.path = getpath(path)

    def __repr__(self):
        return f"py416.files.File('{self.path}')"

    def __str__(self):
        return self.path

    @property
    def atime(self) -> float:
        return os.path.getatime(self.path)

    @property
    def atimes(self) -> tuple:
        return tuple(dt.fromtimestamp(self.atime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def children(self) -> tuple:
        return listdir(self.path) if self.isdir else ()

    @property
    def ctime(self) -> float:
        return os.path.getctime(self.path)

    @property
    def ctimes(self) -> tuple:
        return tuple(dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @property
    def isdir(self) -> bool:
        return os.path.isdir(self.path)

    @property
    def isfile(self) -> bool:
        return os.path.isfile(self.path)

    @property
    def isroot(self) -> bool:
        return self.path == str(self.parent)

    @property
    def mtime(self) -> float:
        return os.path.getmtime(self.path)

    @property
    def mtimes(self) -> tuple:
        return tuple(dt.fromtimestamp(self.mtime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def name(self) -> str:
        return os.path.basename(self.path) if not self.isroot else self.path

    @property
    def parent(self) -> str:
        return File(parent(self.path))

    @property
    def parts(self) -> tuple:
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

    def copy(self, dest:str):
        '''
        - Copies file/directory
        - Input: `dest` (`str`): directory to copy file into
        - The copy is not tracked
        '''
        copy(self.path, dest)
        return self

    def delete(self, force:bool=False):
        '''
        - Deletes file/directory
        - If the object is a directory and all subdirs are empty, recursively deletes them
        - Input: `force` (`bool`): whether to force deletion with `shutil.rmtree()`
        '''
        force = bool(force)
        delete(self.path, force=force)
        return self

    def move(self, dest:str):
        '''
        - Moves file/directory
        - Input: `dest` (`str`): directory to move file into
        '''
        self.path = move(self.path, dest)
        return self

    def rename(self, newname:str):
        '''
        - Renames file, keeping in same directory
        - Input: `new_name` (`str`): new file name
        '''
        self.path = rename(self.path, newname)
        return self

def cd(path:str='..') -> str:
    '''
    - Wrapper for `os.chdir()`
    - Changes current working directory
    - Creates destination if nonexistent
    - Input: `dir` (`str`): directory path
        - Default: up a directory
    - Return: `str` with current working directory (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    path = getpath(path)
    makedirs(path)
    os.chdir(path)
    return path

def checkzip(path:str) -> bool:
    '''
    - Checks if an archive file (.7z or .zip) exists and is valid
    - Imports `py7zr` if `path` ends with .7z
    - Deletes file if invalid or incomplete
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
                delete(path)
                return False
        if path.endswith('.zip'):
            from zipfile import BadZipFile, ZipFile
            try:
                with ZipFile(path) as z:
                    pass
                return True
            except BadZipFile:
                delete(path)
                return False
    except FileNotFoundError:
        return False

def copymove(func):
    '''
    - Wrapper for `py416.paths.copy()` and `py416.paths.move()`
    - Copy and move are very similar, so this handles some of what they share
    '''
    def _copymove(path:str, dest:str, overwrite:bool=False):
        if gettype(path) != gettype(dest) != 'str':
            raise TypeError('input must be a string')
        if not os.path.exists(path):
            raise FileNotFoundError('path does not exist')
        if os.path.exists(dest) and not os.path.isdir(dest):
            raise FileExistsError('you can\'t move something into a file')
        if getpath(path) == getpath(dest):
            raise ValueError('you can\'t move something into itself')
        overwrite = bool(overwrite)
        makedirs(dest)
        return forslash(func(path, dest, overwrite))
    return _copymove

@copymove
def copy(path:str, dest:str, overwrite:bool=False) -> str:
    '''
    - Copies file or directory and all contents, creating destination if nonexistent
    - Adds some extra safety to `shutil` functions with Exceptions
    - Input:
        - `path` (`str`): path to desired file/directory
        - `dest` (`str`): path to destination parent directory (where we're going into)
        - `overwrite` (`bool`): whether to overwrite an existing file/directory
            - Merges directories, but overwrites files if they exist
            - Default: `False`
    - Return: `str` with path to copied file/directory (formatted with `/`)
    '''
    newpath = f'{dest}/{os.path.basename(path)}'
    newpath_exists = os.path.exists(newpath)
    if os.path.isfile(path): # copying file
        if newpath_exists:
            if overwrite:
                return sh.copy2(path, newpath) # overwriting dest file
            raise FileExistsError('destination file already exists') # not overwriting
        return sh.copy2(path, newpath) # dest file doesn't exist, good
    if newpath_exists and overwrite: # copying directory
        return sh.copytree(path, newpath, dirs_exist_ok=True) # overwriting dest dir
    return sh.copytree(path, newpath) # dest dir doesn't exist, or if it does, shutil raises FileExistsError

def delete(path:str, force:bool=False) -> None:
    '''
    - Deletes file or directory
    - Input:
        - `path` (`str`): path to file or directory
        - `force` (`bool`): whether to try `shutil.rmtree()` to delete a directory
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist')
    force = bool(force)
    if os.path.isdir(path):
        if force:
            sh.rmtree(path)
        else:
            rmdir(path)
    else:
        os.remove(path)

def forslash(path:str) -> str:
    '''
    - Replaces `\\` in paths with `/`
    - Used to unify path formatting between OS types
    - Input: `path` (`str`): path string
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    return path.replace('\\', '/')

def getcwd() -> str:
    '''
    - Wrapper for `os.getcwd()`
    - Gets the current working directory
    - Return: `str` with path (formatted with `/`)
    '''
    return forslash(os.getcwd())

def getpath(path:str) -> str:
    '''
    - Gets the full path of something
    - Input: `path` (`str`): absolute or relative path
        - If relative, we assume it's in the current working directory
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    drives = ['/'] + [f'{ch}:/' for ch in 'abcdefghijklmnopqrstuvwxyz']
    if splitpath(path)[0].lower() not in drives: # relative path
        return f'{getcwd()}/{forslash(path)}'
    return forslash(os.path.abspath(path))

def listdir(path:str='.', dirs:bool=True, files:bool=True) -> tuple:
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
    - Return: `tuple` of `str` with paths (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        return []
    dirs = bool(dirs)
    files = bool(files)
    path = getpath(path)
    result = []
    for child in os.listdir(path):
        child = f'{path}/{child}'
        if dirs and os.path.isdir(child):
            result.append(child)
        if files and not os.path.isdir(child):
            result.append(child)
    return tuple(result)

def log(path:str, msg:str, ts:bool=True, ts_args:tuple=(1,0,1,1,1,0)) -> None:
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
        raise ValueError('input must be a string')
    if gettype(ts_args) not in ['list', 'tuple']:
        raise ValueError('input must be a list/tuple')
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

def makedirs(*dirs, ignore_errors:bool=True) -> tuple:
    '''
    - Wrapper for `os.makedirs()`
    - Creates directories if nonexistent
    - Input:
        - `dirs`:
            - `str` directory path
            - Nestings of `list`/`tuple` objects with `str` directory path base elements
        - `ignore_errors` (`bool`): whether to catch all Exceptions in the process
            - Useful to create as many of the requested directories as possible
            - Default: `True`
    - Return: `tuple` of directories we failed to create
    '''
    if gettype(dirs) not in ['list', 'str', 'tuple']:
        raise TypeError('input must be a string, list, or tuple')
    ignore_errors = bool(ignore_errors)
    errored = []
    for dir in unpack(dirs):
        if gettype(dir) != 'str':
            errored.append(dir)
            continue
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception:
                if not ignore_errors:
                    raise
                errored.append(dir)
    return tuple(errored)

@copymove
def move(path:str, dest:str, overwrite:bool=False) -> str:
    '''
    - Moves file or directory and all contents, creating destination if nonexistent
    - Adds some extra safety to `shutil` functions with Exceptions
    - Input:
        - `path` (`str`): path to desired file/directory
        - `dest` (`str`): path to destination parent directory (where we're going into)
        - `overwrite` (`bool`): whether to overwrite an existing file/directory
            - Overwrites files if they exist
            - Default: `False`
    - Return: `str` with path to moved file/directory (formatted with `/`)
    '''
    newpath = f'{dest}/{os.path.basename(path)}'
    newpath_exists = os.path.exists(newpath)
    _move = lambda: sh.move(path, dest)
    if os.path.isfile(path): # moving file
        if newpath_exists:
            if overwrite:
                return _move() # overwriting dest file
            raise FileExistsError('destination file already exists') # not overwriting
        return _move() # dest file doesn't exist, good
    if newpath_exists: # moving directory
        if overwrite:
            result = sh.copytree(path, newpath, dirs_exist_ok=True) # overwriting dest dir
            delete(path, force=True) # deleting original (we're doing copy->delete manually)
            return result
        raise FileExistsError('destination directory already exists') # not overwriting
    return _move() # dest dir doesn't exist, good

def parent(path:str) -> str:
    '''
    - Gets the directory containing something
    - Input: `path` (`str`): path to find the parent of
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    dirname = lambda _path: getpath(os.path.abspath(f'{getpath(_path)}/..'))
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
    parts = (str(item).replace('/', '').replace('\\', '') for item in unpack(parts))
    return '/' if parts == ('') else '/'.join(parts)

def rename(path:str, name:str) -> str:
    '''
    - Wrapper for `os.rename()`
    - Renames file without moving it
    - Input:
        - `path` (`str`): path to file/directory to be renamed
        - `name` (`str`): new basename for file (not path)
    - Return: `str` with new path (formatted with `/`)
    '''
    if gettype(path) != gettype(name) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist')
    newpath = f'{parent(path)}/{name}'
    os.rename(path, newpath)
    return newpath

def rmdir(path:str, delroot:bool=True) -> int:
    '''
    - Wrapper for `os.rmdir()`
    - Recursively deletes empty directories
    - Input:
        - `dirpath` (`str`): directory path to delete within
        - `delroot` (`bool`): whether to delete `path` as well
            - Default: `True`
    - Return: `int` with number of deleted directories
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist')
    if not os.path.isdir(path):
        raise ValueError('path is not a directory')
    delroot = bool(delroot)
    count = 0
    for item in listdir(path):
        if os.path.isdir(item):
            count += rmdir(item)
    if not len(listdir(path)) and delroot:
        if getpath(path) == getcwd():
            cd() # we're in the directory we're trying to delete, so go up
        os.rmdir(path)
        count += 1
    return count

def splitpath(path:str) -> tuple:
    '''
    - Splits a path string into its parts
    - Input: `path` (`str`): path
    - Return: `tuple` of directories/file
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    path = forslash(path)
    parts = forslash(os.path.abspath(path)).split('/')
    parts[0] = f'{parts[0]}/' # root
    if path.startswith('//'): # Windows network location
        result = [f'//{parts[2]}'] # network root
        return tuple(result + [a for a in parts[3:]]) if len(parts) > 2 else tuple(result)
    return (parts[0],) if parts[1] == '' else tuple(parts)

def unzip(path:str, remove:bool=False) -> None:
    '''
    - Unzips archive files of type: (.7z, .gz, .rar, .tar, .zip)
    - Input:
        - `path` (`str`): path to archive file
        - `remove` (`bool`): whether to delete archive after unzipping
            - Default: `False`
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist')
    remove = bool(remove)
    fparent = parent(path)
    if path.endswith('.7z'):
        from py7zr import unpack_7zarchive
        unpack_7zarchive(path, fparent)
        if remove:
            delete(path)
    elif path.endswith(('.gz', '.rar', '.tar', '.zip')):
        sh.unpack_archive(path, fparent)
        if remove:
            delete(path)
    else:
        raise NotImplementedError('unsupported archive format')

def unzipdir(path:str='.', ignore_errors:bool=True) -> int:
    '''
    - Unzips all archives in a directory until it is unable to continue
    - Deletes all archives as it unzips
    - Supports archives of type: (.7z, .gz, .rar, .tar, .zip)
    - Input:
        - `path` (`str`): directory from which to unzip archives
            - Default: current working directory
        - `ignore_errors` (`bool`): whether to catch all Exceptions in unzipping
            - Useful to unzip everything possible in the directory
            - Default: `True`
    - Return: `int` with number of unzipped archives
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    if not os.path.exists(path):
        raise FileNotFoundError('path does not exist')
    ignore_errors = bool(ignore_errors)
    unzipped = 0
    while True:
        unzipped_this_run = 0
        for file in listdir(path, dirs=False):
            try:
                if not unzip(file, remove=True):
                    unzipped += 1
                    unzipped_this_run += 1
            except Exception:
                if not ignore_errors:
                    raise
        if not unzipped_this_run:
            break
    return unzipped

