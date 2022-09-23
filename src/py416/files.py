'''
- Author:  Ezio416
- Created: 2022-08-16
- Updated: 2022-09-23

Functions for file system manipulation
    - OS-agnostic (Windows/Unix) - we always return Windows paths with forward slashes
    - supports absolute and relative paths

Does not yet support any paths that:
    - are not strings
    - contain multiple single or double-dots [ . | .. ]
    - contain single or double-dots in the beginning/middle
'''
from datetime import datetime as dt
import os
import shutil as sh
import sys

from .general import gettype, timestamp, unpack


class File():
    '''
    - class for keeping track of a file/folder and performing actions on it

    Parameters
    ----------
    path : str
        - path to the file/folder we wish to track
    '''
    def __init__(self, path):
        self.path = getpath(path)

    def __repr__(self) -> str:
        return f"py416.files.File('{self.path}')"

    def __str__(self) -> str:
        return self.path

    @property
    def atime(self) -> float:
        '''
        - the last time the file/folder was accessed
        - given in `Unix time <https://www.unixtimestamp.com>`_ (local) as a float
        - i.e. 1663948504.5217497
        '''
        return os.path.getatime(self.path)

    @property
    def atimes(self) -> tuple:
        '''
        - the last time the file/folder was accessed
        - given as a tuple[int], starting with year and ending with microseconds
        - i.e. (2022, 09, 23, 10, 01, 43, 544875)
        '''
        return tuple(dt.fromtimestamp(self.atime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def children(self) -> tuple:
        '''
        - tuple of full paths for everything inside the folder
        - if path is empty or not a folder, returns an empty tuple
        - i.e. ('C:/thisfolder/file1.txt', 'C:/thisfolder/file2.csv') or ( )
        '''
        return listdir(self.path) if self.isdir else ()

    @property
    def ctime(self) -> float:
        '''
        - the time the file/folder was created
        - given in `Unix time <https://www.unixtimestamp.com>`_ (local) as a float
        - i.e. 1663948504.5217497
        '''
        return os.path.getctime(self.path)

    @property
    def ctimes(self) -> tuple:
        '''
        - the time the file/folder was created
        - given as a tuple[int], starting with year and ending with microseconds
        - i.e. (2022, 09, 23, 10, 01, 43, 544875)
        '''
        return tuple(dt.fromtimestamp(self.ctime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def exists(self) -> bool:
        '''
        - whether the file/folder exists
        '''
        return os.path.exists(self.path)

    @property
    def isdir(self) -> bool:
        '''
        - whether the file/folder is a folder
        '''
        return os.path.isdir(self.path)

    @property
    def isfile(self) -> bool:
        '''
        - whether the file/folder is a file
        '''
        return os.path.isfile(self.path)

    @property
    def isroot(self) -> bool:
        '''
        - whether the folder is a root directory
            - on Unix, this is always a single forward slash ( / )
            - on Windows, these are drive letters ( C:/ ) or network locations ( //netloc )
        '''
        return self.path == str(self.parent)

    @property
    def mtime(self) -> float:
        '''
        - the last time the file/folder was modified
        - given in `Unix time <https://www.unixtimestamp.com>`_ (local) as a float
        - i.e. 1663948504.5217497
        '''
        return os.path.getmtime(self.path)

    @property
    def mtimes(self) -> tuple:
        '''
        - the last time the file/folder was modified
        - given as a tuple[int], starting with year and ending with microseconds
        - i.e. (2022, 09, 23, 10, 01, 43, 544875)
        '''
        return tuple(dt.fromtimestamp(self.mtime).strftime('%Y,%m,%d,%H,%M,%S,%f').split(','))

    @property
    def name(self) -> str:
        '''
        - the basename of the file/folder
        - i.e. file.txt or foldername
        '''
        return os.path.basename(self.path) if not self.isroot else self.path

    @property
    def parent(self) -> object:
        '''
        - the parent path of the file/folder
        - creates a new File() instance for the parent path
        '''
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

    def copy(self, dest: str, overwrite: bool = False) -> object:
        '''
        - copies file/folder without tracking the created copy

        Parameters
        ----------
            dest: str
                - folder to copy file/folder into
            overwrite: bool
                - whether to overwrite if the destination file/folder already exists
                - default: False
        
        Returns
        -------
            self: File
        '''
        copy(self.path, dest, overwrite=overwrite)
        return self

    def delete(self, force: bool = False) -> object:
        '''
        - deletes file/folder, attempting to recursively delete empty subfolders

        Parameters
        ----------
            force: bool
                - whether to force deletion with `shutil.rmtree() <https://docs.python.org/3/library/shutil.html#shutil.rmtree>`_
                - default: False
        '''
        delete(self.path, force=force)
        return self

    def move(self, dest: str, overwrite: bool = False) -> object:
        '''
        - moves file/folder, maintaining tracking at the new location

        Parameters
        ----------
            dest: str
                - folder to move file/folder into
            overwrite: bool
                - whether to overwrite if the destination file/folder already exists
                - default: False
        '''
        self.path = move(self.path, dest, overwrite=overwrite)
        return self

    def rename(self, name: str) -> object:
        '''
        - renames file/folder without moving it
        
        Parameters
        ----------
            name: str
                - new basename for the file/folder
        '''
        self.path = rename(self.path, name)
        return self


def cd(path: str = '..') -> str:
    '''
    - Wrapper for `os.chdir()`
    - Changes current working directory
    - Creates destination if nonexistent
    - Input: `dir` (`str`): directory path
        - Default: up a directory
    - Return: `str` with current working directory
    '''
    path = getpath(path)
    makedirs(path)
    os.chdir(path)
    return path


def checkwindrive(drive: str) -> str:
    '''
    - Checks if a given string is a Windows drive letter (i.e. 'C:', 'D:\\\\', 'E:/')
    - Input: `drive` (`str`): string to check
    - Return: `str` with drive
    '''
    drive = forslash(drive).upper()
    if len(drive) not in (2, 3):
        return ''
    if drive[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or drive[1] != ':':
        return ''
    if len(drive) == 3:
        if drive[2] != '/':
            return ''
        return drive
    return drive + '/'


def checkzip(path: str) -> bool:
    '''
    - Checks if an archive file (.7z or .zip) exists and is valid
    - Imports `py7zr` if `path` ends with .7z
    - Deletes file if invalid or incomplete
    - Input: `path` (`str`): path to the archive file
    - Return:
        - `True`: file exists and is valid
        - `False`: file doesn't exist, possibly because we deleted it due to corruption
    '''
    path = getpath(path)
    try:
        if path.endswith('.7z'):
            from py7zr import exceptions, SevenZipFile
            try:
                with SevenZipFile(path, 'r'):
                    pass
                return True
            except exceptions.Bad7zFile:
                delete(path)
                return False
        if path.endswith('.zip'):
            from zipfile import BadZipFile, ZipFile
            try:
                with ZipFile(path):
                    pass
                return True
            except BadZipFile:
                delete(path)
                return False
    except FileNotFoundError:
        return False


def copymove(func):
    '''
    - Wrapper for `py416.files.copy()` and `py416.files.move()`
    - Copy and move are very similar, so this handles some of what they share
    '''
    def _copymove(path: str, dest: str, overwrite: bool = False):
        path = getpath(path)
        dest = getpath(dest)
        overwrite = bool(overwrite)
        if not os.path.exists(path):
            raise FileNotFoundError(f'not found: {path}')
        if path == dest:
            raise ValueError(f'you can\'t move something into itself: {path}')
        if os.path.exists(dest) and not os.path.isdir(dest):
            raise FileExistsError(f'you can\'t move something into a file: {dest}')
        makedirs(dest)
        return forslash(func(path, dest, overwrite))
    return _copymove


@copymove
def copy(path: str, dest: str, overwrite: bool = False) -> str:
    '''
    - Copies file or directory and all contents, creating destination if nonexistent
    - Adds some extra safety to `shutil` functions with Exceptions
    - Input:
        - `path` (`str`): path to desired file/directory
        - `dest` (`str`): path to destination parent directory (where we're going into)
        - `overwrite` (`bool`): whether to overwrite an existing file/directory
            - Merges directories, but overwrites files if they exist
            - Default: `False`
    - Return: `str` with path to copied file/directory
    '''
    new_path = f'{dest}/{os.path.basename(path)}'
    new_path_exists = os.path.exists(new_path)
    if os.path.isfile(path):  # copying file
        if new_path_exists and not overwrite:
            raise FileExistsError(f'destination file already exists: {new_path}')
        return sh.copy2(path, new_path)
    if new_path_exists:  # copying directory
        if overwrite:
            return sh.copytree(path, new_path, dirs_exist_ok=True)  # overwriting dest dir
        raise FileExistsError(f'destination directory already exists: {new_path}')
    return sh.copytree(path, new_path)  # dest dir doesn't exist, good


def delete(path: str, force: bool = False) -> None:
    '''
    - Deletes file or directory
    - Input:
        - `path` (`str`): path to file or directory
        - `force` (`bool`): whether to try `shutil.rmtree()` to delete a directory and its contents
            - Default: `False`
    '''
    path = getpath(path)
    force = bool(force)
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
    if os.path.isdir(path):
        if force:
            sh.rmtree(path)
        else:
            rmdir(path)
    else:
        os.remove(path)


def forslash(path: str) -> str:
    '''
    - Replaces `\\` in paths with `/`
    - Used to unify path formatting between OS types
    - Input: `path` (`str`): path string
    - Return: `str` with path
    '''
    if gettype(path) != 'str':
        raise TypeError(f'input must be a string; invalid: {path}')
    return path.replace('\\', '/')


def getcwd() -> str:
    '''
    - Wrapper for `os.getcwd()`
    - Gets the current working directory
    - Return: `str` with path
    '''
    return forslash(os.getcwd())


def getpath(path: str) -> str:
    '''
    - Gets the full path of something
    - Input: `path` (`str`): absolute or relative path
        - If relative, we assume it's in the current working directory
    - Return: `str` with path
    '''
    parts = list(splitpath(path))
    if parts == ['']:  # special case
        return ''
    path = joinpath(parts)
    root = parts[0]
    if root.startswith('//') or root == '/':  # Windows network location or Unix root
        return path
    cwdrive = checkwindrive(root)
    if cwdrive:  # Windows root
        parts[0] = cwdrive
        return joinpath(parts)
    return f'{getcwd()}/{path}'


def joinpath(*parts) -> str:
    '''
    - Imitator for `os.path.join()`
    - Joins parts of a path together in the order they were received
    - Input: `parts` (iterable): directories/file to join together
    - Return: `str` with path
    '''
    parts = list(unpack([list(splitpath(part)) for part in unpack(parts)]))  # split elements if partial paths
    if parts == ['/', '/']:  # special case
        return '/'
    while '' in parts:
        parts.remove('')  # special case, such as passing 'folder/..' to splitpath()
    if not len(parts):
        return ''  # nothing was passed, or it was cancelled out with '..'
    if parts[0].startswith('//'):
        return '/'.join(parts)  # Windows network location
    if parts == ['/']:
        return '/'  # Unix root, alone
    if parts[0] == '/':
        return '/' + '/'.join(parts[1:])  # Unix root, preceding
    cwdrive = checkwindrive(parts[0])
    if cwdrive:
        if len(parts) == 1:
            return cwdrive  # Windows drive root, alone
        return cwdrive + '/'.join(parts[1:])  # Windows drive root, preceding
    return '/'.join(parts)


def listdir(path: str = '.', dirs: bool = True, files: bool = True) -> tuple:
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
    - Return: `tuple` of `str` with paths
    '''
    path = getpath(path)
    dirs = bool(dirs)
    files = bool(files)
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
    result = []
    for child in os.listdir(path):
        child = joinpath(path, child)
        if dirs and os.path.isdir(child):
            result.append(child)
        if files and not os.path.isdir(child):
            result.append(child)
    return tuple(result)


def log(path: str, msg: str, ts: bool = True, ts_args: tuple = (1, 0, 1, 1, 1, 0)) -> None:
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
    path = getpath(path)
    if gettype(msg) != 'str':
        raise ValueError(f'input must be a string; invalid: {msg}')
    ts = bool(ts)
    if gettype(ts_args) not in ('list', 'tuple'):
        raise ValueError(f'input must be a list/tuple; invalid: {ts_args}')
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


def makedirs(*dirs, ignore_errors: bool = True) -> tuple:
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
    if gettype(dirs) not in ('list', 'str', 'tuple'):
        raise TypeError(f'input must be a string/list/tuple; invalid: {dirs}')
    ignore_errors = bool(ignore_errors)
    errored = []
    for dir in unpack(dirs):
        if gettype(dir) != 'str':
            errored.append(dir)
            continue
        dir = getpath(dir)
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception:
                if not ignore_errors:
                    raise
                errored.append(dir)
    return tuple(errored)


def makefile(path: str, msg: str = '', overwrite: bool = False) -> str:
    '''
    - Wrapper for `open()`
    - Creates a new file
    - Input:
        - `path` (`str`): full path of desired new file
        - `msg` (`str`): text to put in the file
            - Default: nothing
        - `overwrite` (`bool`): whether to overwrite a file if it already exists
            - Default: `False`
    - Return: `str` with path to new file
    '''
    path = getpath(path)
    if gettype(msg) != 'str':
        raise TypeError(f'input must be a string; invalid: {path}')
    overwrite = bool(overwrite)
    if os.path.exists(path) and overwrite:
        delete(path, force=True)
    if os.path.isfile(path):
        raise FileExistsError(f'destination file already exists: {path}')
    if os.path.isdir(path):
        raise IsADirectoryError(f'destination already exists as a directory: {path}')
    makedirs(parent(path))
    with open(path, 'a') as file:
        file.write(msg)
    return path


@copymove
def move(path: str, dest: str, overwrite: bool = False) -> str:
    '''
    - Moves file or directory and all contents, creating destination if nonexistent
    - Adds some extra safety to `shutil` functions with Exceptions
    - Input:
        - `path` (`str`): path to desired file/directory
        - `dest` (`str`): path to destination parent directory (where we're going into)
        - `overwrite` (`bool`): whether to overwrite an existing file/directory
            - Overwrites files if they exist
            - Default: `False`
    - Return: `str` with path to moved file/directory
    '''
    new_path = f'{dest}/{os.path.basename(path)}'
    new_path_exists = os.path.exists(new_path)
    if os.path.isfile(path):  # moving file
        if new_path_exists and not overwrite:
            raise FileExistsError(f'destination file already exists: {new_path}')
        return sh.move(path, dest)
    if new_path_exists:  # moving directory
        if overwrite:
            result = sh.copytree(path, new_path, dirs_exist_ok=True)  # overwriting dest dir
            delete(path, force=True)  # deleting original (we're doing copy->delete manually)
            return result
        raise FileExistsError(f'destination directory already exists: {new_path}')
    return sh.move(path, dest)  # dest dir doesn't exist, good


def parent(path: str) -> str:
    '''
    - Gets the directory containing something
    - Input: `path` (`str`): path to find the parent of
    - Return: `str` with path
    '''
    path = getpath(path)
    if not path:
        return ''
    if any([path == '/',  # Root
            checkwindrive(path),
            path.startswith('//') and len(splitpath(path)) == 1]):
        return path
    return getpath(f'{path}/..')


def rename(path: str, name: str) -> str:
    '''
    - Wrapper for `os.rename()`
    - Renames file without moving it
    - Input:
        - `path` (`str`): path to file/directory to be renamed
        - `name` (`str`): new basename for file (not path)
    - Return: `str` with new path
    '''
    path = getpath(path)
    if gettype(name) != 'str':
        raise TypeError(f'input must be a string; invalid: {name}')
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
    newpath = f'{parent(path)}/{name}'
    os.rename(path, newpath)
    return newpath


def rmdir(path: str, delroot: bool = True) -> int:
    '''
    - Wrapper for `os.rmdir()`
    - Recursively deletes empty directories
    - Input:
        - `dirpath` (`str`): directory path to delete within
        - `delroot` (`bool`): whether to delete `path` as well
            - Default: `True`
    - Return: `int` with number of deleted directories
    '''
    path = getpath(path)
    delroot = bool(delroot)
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
    if not os.path.isdir(path):
        raise ValueError(f'not a directory: {path}')
    count = 0
    for item in listdir(path):
        if os.path.isdir(item):
            count += rmdir(item)
    if not len(listdir(path)) and delroot:
        if path == getcwd():
            cd()  # we're in the directory we're trying to delete, so go up
        os.rmdir(path)
        count += 1
    return count


def splitpath(path: str) -> tuple:
    '''
    - Splits a path string into its parts
    - Input: `path` (`str`): path
    - Return: `tuple` of directories/file
    '''
    if not path:
        return '',
    path = forslash(path)
    win_net = False

    if path in ('/', '/.', '/..'):  # special cases
        return '/',
    parts = path.split('/')
    if path == '.':  # current directory
        path = getcwd()
    elif path == '..':  # parent of current directory
        path = forslash(os.path.dirname(getcwd()))
    elif parts[-1] == '.':  # path/. is just path
        path = path[:-2]
    elif parts[-1] == '..':  # parent of path
        if len(parts) == 2:  # 'folder/..'
            return '',
        if path.startswith('//'):  # Windows network location
            path = path.lstrip('/')
            win_net = True
        path = os.path.dirname(os.path.dirname(path))
        if win_net:
            path = '//' + path
    parts = path.split('/')

    if not parts[0]:  # Unix root
        parts[0] = '/'
    cwdrive = checkwindrive(parts[0])
    if cwdrive:  # Windows drive root
        parts[0] = cwdrive
    if path.startswith('//'):  # Windows network location
        result = [f'//{parts[2]}']
        return tuple(result + [a for a in parts[3:]]) if len(parts) > 2 else tuple(result)
    if len(parts) == 2:
        if parts[1] == '':
            return parts[0],
    return tuple(parts)


def unzip(path: str, remove: bool = False) -> None:
    '''
    - Unzips archive files of type: (.7z, .gz, .rar, .tar, .zip)
    - Imports `py7zr` if a file ends with .7z
    - Input:
        - `path` (`str`): path to archive file
        - `remove` (`bool`): whether to delete archive after unzipping
            - Default: `False`
    '''
    path = getpath(path)
    remove = bool(remove)
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
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
        raise NotImplementedError(f'unsupported archive format: {path.split(".")[-1]}')


def unzipdir(path: str, ignore_errors: bool = True) -> int:
    '''
    - Unzips all archives in a directory (only 1st level) until it is unable to continue
    - Deletes all archives as it unzips
    - Supports archives of type: (.7z, .gz, .rar, .tar, .zip)
    - Imports `py7zr` if a file ends with .7z
    - Input:
        - `path` (`str`): directory containing archive files
        - `ignore_errors` (`bool`): whether to catch all Exceptions in unzipping
            - Useful to unzip everything possible in the directory
            - Default: `True`
    - Return: `int` with number of unzipped archives
    '''
    path = getpath(path)
    ignore_errors = bool(ignore_errors)
    if not os.path.exists(path):
        raise FileNotFoundError(f'not found: {path}')
    unzipped = 0
    while True:
        unzipped_this_run = 0
        for file in listdir(path, dirs=False):
            try:
                if not unzip(file, remove=True):
                    unzipped += 1
                    unzipped_this_run += 1
            except ModuleNotFoundError:
                raise
            except Exception:
                if not ignore_errors:
                    raise
        if not unzipped_this_run:
            break
    return unzipped
