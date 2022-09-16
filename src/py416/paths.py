'''
Name:    py416.paths
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-09-15

Functions for file system manipulation
OS-agnostic (Windows/Unix) - Windows paths will always have forward slashes
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
        return f"py416.filesystem.File('{self.path}')"

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
    def ctime(self) -> float:
        return os.path.getctime(self.path)

    @property
    def ctimes(self) -> list:
        return dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(',')

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
        - Input: `force` (`bool`): whether to force deletion with `shutil.rmtree()`
        '''
        force = bool(force)
        delete(self.path, force=force)
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

def cd(dir:str='..') -> str:
    '''
    - Wrapper for `os.chdir()`
    - Changes current working directory
    - Creates destination if nonexistent
    - Input: `dir` (`str`): directory path
        - Default: up a directory
    - Return: `str` with current working directory (formatted with `/`)
    '''
    if gettype(dir) != 'str':
        raise TypeError('input must be a string')
    dir = getpath(dir)
    makedirs(dir)
    os.chdir(dir)
    return dir

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

def copy(path:str, dest:str, overwrite:bool=False) -> str:
    '''
    - Wrapper for `shutil.copy2()`
    - Copies file, creating destination if nonexistent
    - Input:
        - `path` (`str`): path to file
        - `dest` (`str`): path to destination directory
        - `overwrite` (`bool`): whether to overwrite an existing file
    - Return: `str` with path to copied file (formatted with `/`)
    '''
    if gettype(path) != gettype(dest) != 'str':
        raise TypeError('input must be a string')
    overwrite = bool(overwrite)
    if not os.path.exists(path):
        raise FileNotFoundError('file does not exist')
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise FileExistsError('destination exists as a file')
    makedirs(dest)
    newpath = f'{dest}/{os.path.basename(path)}'
    if os.path.exists(newpath) and not overwrite:
        raise FileExistsError('destination file already exists')
    sh.copy2(path, newpath)
    return newpath

def delete(path:str, force:bool=False) -> None:
    '''
    - Deletes file or directory
    - Input:
        - `path` (`str`): path to file or directory
        - `force` (`bool`): whether to try `shutil.rmtree()` to delete a directory
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    force = bool(force)
    if os.path.exists(path):
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
        raise TypeError('input must be a string')
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

def makedirs(*dirs, ignore_errors:bool=True) -> list:
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
    - Return: `list` of directories we failed to create
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
    return errored

def move(path:str, dest:str, overwrite:bool=False) -> str:
    '''
    - Wrapper for `shutil.move()`
    - Moves file with some extra safety in the form of Exceptions
    - Input:
        - `path` (`str`): path to file/directory
        - `dest` (`str`): path to destination directory
    - Return: `str` with path to destination file (formatted with `/`)
    '''
    if gettype(path) != gettype(dest) != 'str':
        raise TypeError('input must be a string')
    overwrite = bool(overwrite)
    if not os.path.exists(path):
        raise FileNotFoundError('file does not exist')
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise FileExistsError('destination exists as a file')
    makedirs(dest)
    if os.path.exists(f'{dest}/{os.path.basename(path)}'):
        raise FileExistsError('destination file already exists')
    return forslash(sh.move(path, dest))

def parent(path:str) -> str:
    '''
    - Gets the directory containing something
    - Input: `path` (`str`): path to find the parent of
    - Return: `str` with path (formatted with `/`)
    '''
    if gettype(path) != 'str':
        raise TypeError('input must be a string')
    dirname = lambda path_: getpath(os.path.abspath(f'{getpath(path_)}/..'))
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
    parts = [str(item).replace('/', '').replace('\\', '') for item in unpack(parts)]
    return '/' if parts == [''] else '/'.join(parts)

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
    new_path = f'{parent(path)}/{name}'
    os.rename(path, new_path)
    return new_path

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
    count = 0
    if os.path.exists(path) and not os.path.isdir(path):
        raise ValueError('path is not a directory')
    files = listdir(path)
    if len(files):
        for item in files:
            if os.path.isdir(item):
                count += rmdir(item)
    files = os.listdir(path)
    if not len(files) and delroot:
        if getpath(path) == getcwd():
            cd() # we're in the directory we're trying to delete, so go up
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
        raise TypeError('input must be a string')
    path = forslash(path)
    parts = forslash(os.path.abspath(path)).split('/')
    parts[0] = f'{parts[0]}/' # root
    if path.startswith('//'): # Windows network location
        result = [f'//{parts[2]}'] # network root
        return result + [a for a in parts[3:]] if len(parts) > 2 else result
    return [parts[0]] if parts[1] == '' else parts

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

