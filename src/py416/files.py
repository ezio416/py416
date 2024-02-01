'''
| Author:  Ezio416
| Created: 2022-08-16
| Updated: 2024-01-31

- Functions for filesystem and path string manipulation

    - OS-agnostic (Windows/Unix) - we always return Windows paths with forward slashes
    - supports absolute and relative paths

- Does not yet support any paths that:

    - are not strings
    - contain multiple single or double-dots ( . | .. )
    - contain single or double-dots in the beginning/middle
'''
from datetime import datetime as dt
from fnmatch import fnmatch, fnmatchcase
from functools import wraps
import os
from shutil import copy2, copytree, move as shmv, rmtree, unpack_archive
from time import time
from zipfile import BadZipFile, ZipFile

from py7zr import exceptions, SevenZipFile, unpack_7zarchive
from send2trash import send2trash

from .general import secmod, secmod_inverse, timestamp, unpack


class File():
    '''
    - class for keeping track of a file/folder and performing actions on it

    Parameters
    ----------
    path: str
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
        - wraps `os.path.getatime() <https://docs.python.org/3/library/os.path.html#os.path.getatime>`_
        - given in `Unix time <https://www.unixtimestamp.com>`_ as a float
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
        - wraps `os.path.getctime() <https://docs.python.org/3/library/os.path.html#os.path.getctime>`_
        - given in `Unix time <https://www.unixtimestamp.com>`_ as a float
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
        - wraps `os.path.exists() <https://docs.python.org/3/library/os.path.html#os.path.exists>`_
        '''
        return os.path.exists(self.path)

    @property
    def isdir(self) -> bool:
        '''
        - whether the file/folder exists and is a folder
        - wraps `os.path.isdir() <https://docs.python.org/3/library/os.path.html#os.path.isdir>`_
        '''
        return os.path.isdir(self.path)

    @property
    def isfile(self) -> bool:
        '''
        - whether the file/folder exists and is a file
        - wraps `os.path.isfile() <https://docs.python.org/3/library/os.path.html#os.path.isfile>`_
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
        - wraps `os.path.getmtime() <https://docs.python.org/3/library/os.path.html#os.path.getmtime>`_
        - given in `Unix time <https://www.unixtimestamp.com>`_ as a float
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
        - i.e. 'file.txt' or 'foldername'
        '''
        return self.parts[-1]

    @property
    def parent(self) -> object:
        '''
        - the parent path of the file/folder
        - creates a new File instance for the parent path
        '''
        return File(parent(self.path))

    @property
    def parts(self) -> tuple:
        '''
        - the parts of the file/folder's path
        - given as a tuple[str]
        - i.e. ('C:/', 'folder', 'file.txt')
        '''
        return splitpath(self.path)

    @property
    def root(self) -> str:
        '''
        - the root of the file/folder's path
        - i.e. 'C:/' or '//netloc' or '/'
        '''
        return self.parts[0]

    @property
    def size(self) -> int:
        '''
        - the size of the file/folder in bytes
        - wraps `os.path.getsize() <https://docs.python.org/3/library/os.path.html#os.path.getsize>`_
        '''
        return os.path.getsize(self.path)

    @property
    def stem(self) -> str:
        '''
        - the basename of the file/folder without the extension
        - i.e. 'file' instead of 'file.txt'
        '''
        return self.name if self.isdir else self.name.split('.')[0]

    @property
    def suffix(self) -> str:
        '''
        - the extension of the file, or blank if a folder
        - i.e. '.txt'
        '''
        return '.' + self.name.split('.')[-1] if not self.isdir else ''

    def copy(self, dest: str, overwrite: bool = False) -> object:
        '''
        - copies file/folder without tracking the created copy
        - in-place operation

        Parameters
        ----------
        dest: str
            - folder to copy file/folder into

        overwrite: bool
            - whether to overwrite if the destination file/folder already exists
            - default: False
        '''
        copy(self.path, dest, overwrite=overwrite)
        return self

    def delete(self, force: bool = False, trash: bool = False) -> object:
        '''
        - deletes file/folder, attempting to recursively delete empty subfolders
        - in-place operation

        Parameters
        ----------
        force: bool
            - whether to force deletion with `shutil.rmtree() <https://docs.python.org/3/library/shutil.html#shutil.rmtree>`_
            - default: False

        trash: bool
            - whether to try moving item to trash/recycle bin (if enabled for that drive)
            - uses `Send2Trash <https://github.com/arsenetar/send2trash>`_
            - UNSAFE - deletes file if trash/recycle bin disabled
            - default: False
        '''
        delete(self.path, force=force, trash=trash)
        return self

    def move(self, dest: str, overwrite: bool = False) -> object:
        '''
        - moves file/folder, maintaining tracking at the new location
        - in-place operation

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
        - in-place operation

        Parameters
        ----------
        name: str
            - new basename for the file/folder
        '''
        self.path = rename(self.path, name)
        return self


def cd(path: str = '..') -> str:
    '''
    - changes the current working directory, creating it if nonexistent
    - wraps `os.chdir() <https://docs.python.org/3/library/os.html#os.chdir>`_

    Parameters
    ----------
    path: str
        - path to folder we want to go in
        - default: parent (up a folder)

    Returns
    -------
    str
        - path to new current working directory
    '''
    makedirs(path := getpath(path))
    os.chdir(path)
    return path


def checkwindrive(drive: str) -> str:
    '''
    - checks if a given string is a Windows drive letter (i.e. 'C:', 'D:\\\\', 'E:/')

    Parameters
    ----------
    drive: str
        - string to check

    Returns
    -------
    str
        - normalized root path ( 'C:/' ) if valid, else an empty string
    '''
    if (len_drive := len(drive := forslash(drive).upper())) not in (2, 3):
        return ''
    if drive[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or drive[1] != ':':
        return ''
    if len_drive == 3:
        if drive[2] != '/':
            return ''
        return drive
    return drive + '/'


def checkzip(path: str) -> bool:
    '''
    - checks if an archive file (.7z or .zip) exists and is valid
    - deletes file if invalid or incomplete
    - does nothing to files with the wrong extension

    Parameters
    ----------
    path: str
        - path to the archive file

    Returns
    -------
    True
        - file exists and is valid

    False
        - file doesn't exist, because either:
            - we deleted it
            - it didn't exist before
    '''
    try:
        if (path := getpath(path)).lower().endswith('.7z'):
            try:
                with SevenZipFile(path, 'r'):
                    pass
                return True  # 7z file is good
            except exceptions.Bad7zFile:
                delete(path)
                return False
        elif path.lower().endswith('.zip'):
            try:
                with ZipFile(path):
                    pass
                return True  # zip file is good
            except BadZipFile:
                delete(path)
                return False
        else:
            raise NotImplementedError(f'unsupported archive format: {path.split(".")[-1]}')
    except FileNotFoundError:
        return False


def copymove(func):
    '''
    - wrapper for :func:`py416.files.copy` and :func:`py416.files.move`
    - copy and move are nearly the same, so this handles some of what they share
    '''
    @wraps(func)
    def _copymove(path: str, dest: str, overwrite: bool = False):
        if not os.path.exists(path := getpath(path)):
            raise FileNotFoundError(f'not found: {path}')
        if path == (dest := getpath(dest)):
            raise ValueError(f'you can\'t move something into itself: {path}')
        if os.path.exists(dest) and not os.path.isdir(dest):
            raise FileExistsError(f'you can\'t move something into a file: {dest}')
        makedirs(dest)
        return forslash(func(path, dest, bool(overwrite)))
    return _copymove


@copymove
def copy(path: str, dest: str, overwrite: bool = False) -> str:
    '''
    - copies file/folder and all contents, creating destination if nonexistent

    Parameters
    ----------
    path: str
        - path to desired file/folder

    dest: str
        - path to destination folder (where we're copying into)

    overwrite: bool
        - whether to overwrite an existing file/folder
        - merges folders, but overwrites files if they exist
        - default: False

    Returns
    -------
    str
        - path to copied file/folder
    '''
    new_path_exists = os.path.exists(new_path := f'{dest}/{os.path.basename(path)}')
    if os.path.isfile(path):  # copying file
        if new_path_exists and not overwrite:
            raise FileExistsError(f'destination file already exists: {new_path}')
        return copy2(path, new_path)
    if new_path_exists:  # copying folder
        if overwrite:
            return copytree(path, new_path, dirs_exist_ok=True)  # overwriting dest folder
        raise FileExistsError(f'destination folder already exists: {new_path}')
    return copytree(path, new_path)  # dest folder doesn't exist, good


def delete(path: str, force: bool = False, trash: bool = False) -> None:
    '''
    - deletes file/folder

    Parameters
    ----------
    path: str
        - path to file/folder

    force: bool
        - whether to try `shutil.rmtree() <https://docs.python.org/3/library/shutil.html#shutil.rmtree>`_ to delete a folder and its contents
        - default: False

    trash: bool
        - whether to try moving item to trash/recycle bin (if enabled for that drive)
        - uses `Send2Trash <https://github.com/arsenetar/send2trash>`_
        - UNSAFE - deletes file if trash/recycle bin disabled
        - default: False
    '''
    if not os.path.exists(path := getpath(path)):
        return
    if bool(trash):
        if os.name == 'nt':
            path = path.replace('/', '\\')
        return send2trash(path)
    if os.path.isdir(path):
        if bool(force):
            rmtree(path)
        else:
            rmdir(path)
    else:
        os.remove(path)


def forslash(path: str) -> str:
    '''
    - replaces backslashes in paths with forward slashes
    - used to unify path formatting between OS types

    Parameters
    ----------
    path: str
        - path string

    Returns
    -------
    str
        - path with forward slashes
    '''
    if type(path) is not str:
        raise TypeError(f'input must be a string; invalid: {path}')
    return path.replace('\\', '/')


def getcwd() -> str:
    '''
    - gets the current working directory
    - wraps `os.getcwd() <https://docs.python.org/3/library/os.html#os.getcwd>`_

    Returns
    -------
    str
        - path to current working directory
    '''
    return forslash(os.getcwd())


def getpath(path: str) -> str:
    '''
    - gets the full path of something, resolving most relative paths

    Parameters
    ----------
    path: str
        - absolute or relative path
        - if relative, we assume it's in the current working directory

    Returns
    -------
    str
        - absolute path
    '''
    if (parts := list(splitpath(path))) == ['']:  # special case
        return ''
    path = joinpath(parts)
    if (root := parts[0]).startswith('//') or root == '/':  # UNC or Unix root
        return path
    if (cwdrive := checkwindrive(root)):  # Windows root
        parts[0] = cwdrive
        return joinpath(parts)
    return f'{getcwd()}/{path}'


def joinpath(*parts) -> str:
    '''
    - joins parts of a path together in the order they were received

    Parameters
    ----------
    parts: iterable
        - folder/file names to join together
        - iterable may be single or nested lists or tuples

    Returns
    -------
    str
        - joined path
    '''
    parts = list(unpack([list(splitpath(part)) for part in unpack(parts)]))  # split elements if partial paths
    if parts == ['/', '/']:  # special case
        return '/'
    while '' in parts:
        parts.remove('')  # special case, such as passing 'folder/..' to splitpath()
    if not len(parts):
        return ''  # nothing was passed, or it was cancelled out with '..'
    if parts == ['/']:
        return '/'  # Unix root, alone
    if parts[0] == '/':
        return '/' + '/'.join(parts[1:])  # Unix root, preceding
    if parts[0].startswith('//'):
        return '/'.join(parts)  # UNC
    if (cwdrive := checkwindrive(parts[0])):
        if len(parts) == 1:
            return cwdrive  # Windows drive root, alone
        return cwdrive + '/'.join(parts[1:])  # Windows drive root, preceding
    return '/'.join(parts)


def listdir(path: str = '.', dirs: bool = True, files: bool = True, recursive: bool = False, search: str = '', case: bool = False, recency=0, return_dict: bool = False, sort_dict: str = 'path'):
    '''
    - lists files/folders within a folder
    - allows for some filtering by filename and modify date
    - wraps `os.listdir() <https://docs.python.org/3/library/os.html#os.listdir>`_

    Parameters
    ----------
    path: str
        - folder to search in
        - default: current working directory

    dirs: bool
        - whether to list folders
        - default: True

    files: bool
        - whether to list files
        - default: True

    recursive: bool
        - whether to list all files and folders recursively
        - if False, this will only list files/folders in the specified folder
        - default: False

    search: str
        - like a glob, searches filenames for a specified pattern
        - this does not search any files, rather the list of files we already gathered
        - accepts Unix wildcards ( * ? [...] [!...] )
        - default: nothing

    case: bool
        - whether to exactly match capitalization of search term
        - does nothing if `search` is not set
        - default: False

    recency: float | int | str
        - how old a file may be, so this only shows the most recently created/modified files
        - type: float | int
            - number of seconds
        - type: str
            - must be formatted like the base output from :func:`py416.secmod`, i.e. "3d16h5m47s"
            - can be missing parts, i.e. "3d47s"
            - capitalization is ignored
            - if multiple of the same type of value are passed in the string, i.e. "4h16h", only the first value is grabbed
        - default: 0 (include everything)

    return_dict: bool
        - whether to return a dictionary instead of a tuple
        - dict contains details on each file with paths as keys and dicts of their details as values
        - structured like so:
            - {path: {'size': int, 'mtime': int, 'mage': str}}
            - size: int
                - bytes
            - mtime: int
                - modify time
                - Unix timestamp
            - mage: str
                - how long ago the modify time was
                - return is from :func:`py416.secmod`, i.e. '46d19h08m07s'
        - default: False

    sort_dict: str
        - what to sort a returned dictionary by
        - accepted values: path, size, mtime, mage
        - always sorts in ascending order (small -> large)
        - sorting by mage (modify age) is reverse to sorting by mtime (modify time)
        - default: path

    Returns
    -------
        - dict[str: dict[str: int, str: int, str: str]]
            - absolute path, size, modify time, modify age
        - tuple[str]
            - absolute paths
    '''
    if not os.path.exists(path := getpath(path)):
        return ()
    if type(search) is not str:
        raise TypeError(f'input must be a string; invalid: {search}')
    if (recency_type := type(recency)) not in (float, int, str):
        raise TypeError(f'input must be a number or string; invalid: {recency}')
    if (sort_dict := str(sort_dict).lower()) not in ('path', 'size', 'mtime', 'mage'):
        raise ValueError(f'invalid sort option: {sort_dict}')
    result = []
    now = time()
    for child in os.listdir(path):
        child = joinpath(path, child)
        if os.path.isdir(child):
            if bool(dirs):
                result.append(child)
            if bool(recursive):
                result += list(listdir(child, dirs=dirs, files=files, recursive=True))
        elif bool(files):
            result.append(child)
    if search:
        tmp = []
        for fpath in result:
            name = os.path.basename(fpath)
            if bool(case):
                if fnmatchcase(name, search):
                    tmp.append(fpath)
                continue
            if fnmatch(name, search):
                tmp.append(fpath)
        result = tmp
    if recency:
        tmp = []
        recency = secmod_inverse(recency) if recency_type is str else float(recency)
        for fpath in result:
            if now - os.path.getmtime(fpath) < recency:
                tmp.append(fpath)
        result = tmp
    if bool(return_dict):
        mydict = {}
        tmp = []
        for fpath in result:
            stat = os.stat(fpath)
            tmp.append((fpath, stat.st_size, (mtime := stat.st_mtime), secmod(now - mtime)[0]))
        if sort_dict == 'size':
            tmp = sorted(tmp, key=lambda i: i[1])
        elif sort_dict == 'mtime':
            tmp = sorted(tmp, key=lambda i: i[2])
        elif sort_dict == 'mage':
            tmp = sorted(tmp, key=lambda i: i[2], reverse=True)
        for file in tmp:
            mydict[file[0]] = {'size': file[1], 'mtime': int(file[2]), 'mage': file[3]}
        return mydict
    return tuple(result)


def log(path: str, msg: str, ts: bool = True, ts_args: tuple = (1, 0, 1, 1, 1, 0), encoding: str = 'utf-8') -> None:
    '''
    - logs to file with current timestamp
    - creates file and its parent folder if nonexistent

    Parameters
    ----------
    path: str
        - path to desired log file

    msg: str
        - message to log

    ts: bool
        - whether to include timestamp
        - default: True

    ts_args: iterable
        - arguments to pass to :func:`py416.timestamp`
        - default return example: [2022-08-19 13:24:54 -06:00]

    encoding: str
        - character set
        - default: utf-8
    '''
    if type(msg) is not str:
        raise ValueError(f'input must be a string; invalid: {msg}')
    if type(ts_args) not in (list, tuple):
        raise ValueError(f'input must be a list/tuple; invalid: {ts_args}')
    makedirs(parent(path := getpath(path)))
    with open(path, 'a', encoding=encoding) as file:
        file.write(f'{timestamp(*ts_args) + "  " if bool(ts) else ""}{msg}\n')


def makedirs(*dirs, ignore_errors: bool = True) -> tuple:
    '''
    - creates directories if nonexistent
    - wraps `os.makedirs() <https://docs.python.org/3/library/os.html#os.makedirs>`_

    Parameters
    ----------
    dirs: list | str | tuple
        - type: str
            - path to folder
        - type: list | tuple
            - nestings of lists and tuples with folder path strings as base elements

    ignore_errors: bool
        - whether to catch all Exceptions from :func:`os.makedirs()`
        - useful to create as many of the requested folders as possible
        - default: True

    Returns
    -------
    tuple
        - folders we failed to create
    '''
    if type(dirs) not in (list, str, tuple):
        raise TypeError(f'input must be a string/list/tuple; invalid: {dirs}')
    errored = []
    for dir in unpack(dirs):
        if type(dir) is not str:
            errored.append(dir)
            continue
        if not os.path.exists(dir := getpath(dir)):
            try:
                os.makedirs(dir)
            except Exception:
                if not bool(ignore_errors):
                    raise
                errored.append(dir)
    return tuple(errored)


def makefile(path: str, msg: str = '', overwrite: bool = False, encoding: str = 'utf-8') -> str:
    '''
    - creates a new file
    - wraps `open() <https://docs.python.org/3/library/functions.html#open>`_

    Parameters
    ----------
    path: str
        - path to desired new file

    msg: str
        - text to put in the file
        - default: nothing

    overwrite: bool
        - whether to overwrite a file if it already exists
        - default: False

    encoding: str
        - character set
        - default: utf-8

    Returns
    -------
    str
        - path to new file
    '''
    if type(msg) is not str:
        raise TypeError(f'input must be a string; invalid: {msg}')
    if os.path.exists(path := getpath(path)) and bool(overwrite):
        delete(path, force=True)
    if os.path.isfile(path):
        raise FileExistsError(f'destination file already exists: {path}')
    if os.path.isdir(path):
        raise IsADirectoryError(f'destination already exists as a directory: {path}')
    makedirs(parent(path))
    with open(path, 'a', encoding=encoding) as file:
        file.write(msg)
    return path


@copymove
def move(path: str, dest: str, overwrite: bool = False) -> str:
    '''
    - moves file/folder and all contents, creating destination if nonexistent

    Parameters
    ----------
    path: str
        - path to desired file/folder

    dest: str
        - path to destination folder (where we're moving into)

    overwrite: bool
        - whether to overwrite an existing file/folder
        - merges folders, but overwrites files if they exist
        - default: False

    Returns
    -------
    str
        - path to moved file/folder
    '''
    new_path_exists = os.path.exists(new_path := f'{dest}/{os.path.basename(path)}')
    if os.path.isfile(path):  # moving file
        if new_path_exists:
            if not overwrite:
                raise FileExistsError(f'destination file already exists: {new_path}')
            delete(new_path)  # deleting dest file to overwrite it
        return shmv(path, dest)
    if new_path_exists:  # moving folder
        if overwrite:
            result = copytree(path, new_path, dirs_exist_ok=True)  # overwriting dest folder
            delete(path, force=True)  # deleting original (we're doing copy->delete manually)
            return result
        raise FileExistsError(f'destination folder already exists: {new_path}')
    return shmv(path, dest)  # dest folder doesn't exist, good


def parent(path: str = '.') -> str:
    '''
    - gets the folder containing something

    Parameters
    ----------
    path: str
        - path to find the parent of
        - default: current working directory

    Returns
    -------
    str
        - parent path
    '''
    if not (path := getpath(path)):
        return ''
    if any([path == '/',  # Root
            checkwindrive(path),
            path.startswith('//') and len(splitpath(path)) == 1]):
        return path
    return getpath(f'{path}/..')


def readfile(path: str, encoding: str = 'utf-8') -> str:
    '''
    - reads text from a file
    - wraps `open() <https://docs.python.org/3/library/functions.html#open>`_

    Parameters
    ----------
    path: str
        - path to file

    encoding: str
        - character set
        - default: utf-8

    Returns
    -------
    str
        - all text from the file
    '''
    if not os.path.exists(path := getpath(path)):
        raise FileNotFoundError(f'not found: {path}')
    with open(path, 'r', encoding=encoding) as file:
        result = file.read()
    return result


def rename(path: str, name: str) -> str:
    '''
    - renames file/folder without moving it
    - wraps `os.rename() <https://docs.python.org/3/library/os.html#os.rename>`_

    Parameters
    ----------
    path: str
        - path to file/folder to be renamed

    name: str
        - new basename for file/folder (not path)

    Returns
    -------
    str
        - new path to file/folder
    '''
    if not os.path.exists(path := getpath(path)):
        raise FileNotFoundError(f'not found: {path}')
    if type(name) is not str:
        raise TypeError(f'input must be a string; invalid: {name}')
    os.rename(path, (newpath := joinpath(parent(path), name)))
    return newpath


def rmdir(path: str, delroot: bool = True) -> int:
    '''
    - recursively deletes empty directories
    - wraps `os.rmdir() <https://docs.python.org/3/library/os.html#os.rmdir>`_

    Parameters
    ----------
    path: str
        - folder path to delete within

    delroot: bool
        - whether to delete the folder specified as well
        - default: True

    Returns
    -------
    int
        - number of deleted folders
    '''
    if not os.path.exists(path := getpath(path)):
        raise FileNotFoundError(f'not found: {path}')
    if not os.path.isdir(path):
        raise ValueError(f'not a folder: {path}')
    count = 0
    for item in listdir(path):
        if os.path.isdir(item):
            count += rmdir(item)
    if not len(listdir(path)) and bool(delroot):
        if path == getcwd():
            cd()  # we're in the folder we're trying to delete, so go up
        os.rmdir(path)
        count += 1
    return count


def splitpath(path: str) -> tuple:
    '''
    - splits a path string into its parts

    Parameters
    ----------
    path: str
        - path
        - can be absolute or relative

    Returns
    -------
    tuple[str]
        - folders/file
    '''
    if not path:
        return '',
    if (path := forslash(path)) in ('/', '/.', '/..'):  # special cases
        return '/',
    win_net = False
    if path == '.':  # current directory
        path = getcwd()
    elif path == '..':  # parent of current directory
        path = forslash(os.path.dirname(getcwd()))
    elif path == '.' * len(path):  # >2 dots - current directory
        path = getcwd()
    elif (parts := path.split('/'))[-1] == '.':  # folder/. is just folder
        path = path[:-2]
    elif parts[-1] == '..':  # parent of path
        if len(parts) == 2:  # 'folder/..'
            return '',
        if path.startswith('//'):  # UNC
            path = path.lstrip('/')
            win_net = True
        path = os.path.dirname(os.path.dirname(path))
        if win_net:
            path = '//' + path
    parts = path.split('/')
    if not parts[0]:  # Unix root
        parts[0] = '/'
    if (cwdrive := checkwindrive(parts[0])):  # Windows drive root
        parts[0] = cwdrive
    if path.startswith('//'):  # UNC
        result = [f'//{parts[2]}']
        return tuple(result + parts[3:]) if len(parts) > 2 else tuple(result)
    if len(parts) == 2:
        if parts[1] == '':
            return parts[0],
    return tuple(parts)


def unzip(path: str, remove: bool = False) -> None:
    '''
    - unzips archive files of type: (.7z, .gz, .rar, .tar, .zip)

    Parameters
    ----------
    path: str
        - path to archive file

    remove: bool
        - whether to delete archive after unzipping
        - default: False
    '''
    if not os.path.exists(path := getpath(path)):
        raise FileNotFoundError(f'not found: {path}')
    remove = bool(remove)
    fparent = parent(path)
    if path.endswith('.7z'):
        unpack_7zarchive(path, fparent)
        if remove:
            delete(path)
    elif path.endswith(('.gz', '.rar', '.tar', '.zip')):
        unpack_archive(path, fparent)
        if remove:
            delete(path)
    else:
        raise NotImplementedError(f'unsupported archive format: {path.split(".")[-1]}')


def unzipdir(path: str = '.', ignore_errors: bool = True) -> int:
    '''
    - unzips all archive files in a folder until it is unable to continue
    - recursive on archive files, but not folders
    - deletes all archive files as it unzips
    - supports archive files of type: (.7z, .gz, .rar, .tar, .zip)

    Parameters
    ----------
    path: str
        - folder containing archive files
        - default: current working directory

    ignore_errors: bool
        - whether to catch all Exceptions in unzipping
        - useful to unzip everything possible in the directory
        - default: True

    Returns
    -------
    int
        - number of unzipped archives
    '''
    if not os.path.exists(path := getpath(path)):
        raise FileNotFoundError(f'not found: {path}')
    unzipped = 0
    while True:
        unzipped_this_run = 0
        for file in listdir(path, dirs=False):
            if not file.endswith(('.7z', '.gz', '.rar', '.tar', '.zip')):
                continue
            try:
                unzip(file, remove=True)
                unzipped += 1
                unzipped_this_run += 1
            except Exception as e:
                if not bool(ignore_errors):
                    raise Exception(f'unzipped {unzipped} archive file(s) before failing: {e}')
        if not unzipped_this_run:
            break
    return unzipped
