'''
Name:    lance_func
Author:  Lance Hoover
Created: 2022
Updated: 2022-07-27
Version: 7.0

A collection of my custom-built functions
Includes some code stolen from the Internet
'''

from datetime import datetime as dt
import os
import sys

def cd(dir:str) -> bool:
    '''
    - `EXCEPTION-SAFE`
    - Change current working directory to `dir`
    - Returns
        - `True` for success
        - `False` for error
    '''
    try:
        os.chdir(dir)
        return True
    except:
        return False

def del_empty_arch(dir:str, extension:str='.7z', bytes:int=58) -> int:
    '''
    - `EXCEPTION-UNSAFE`
    - Recursively deletes all empty .7z files created by py7zr
    - Returns `int` of deleted files
    '''
    count = 0
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            zpath = f'{subdir}\\{file}'
            if zpath.endswith(extension) and os.path.getsize(zpath) == bytes:
                remove(zpath)
                count += 1
    return count

def del_empty_fold(folder_path:str, remove_root:bool=True) -> int:
    '''
    - `EXCEPTION-UNSAFE`
    - Recursively deletes all empty folders inside `folder_path`
    - Deletes `folder_path` based on `remove_root` and if empty
    - Returns `int` of deleted folders
    '''
    count = 0
    if not os.path.isdir(folder_path):
        return 0
    files = os.listdir(folder_path)
    if len(files):
        for file in files:
            fpath = f'{folder_path}\\{file}'
            if os.path.isdir(fpath):
                count += del_empty_fold(fpath)
    files = os.listdir(folder_path)
    if not len(files) and remove_root:
        try:
            os.rmdir(folder_path)
            count += 1
        except Exception as e:
            print(e)
    return count

def get_listuple_type(item):
    '''
    - `EXCEPTION-SEMISAFE`
    - Checks if item is a list or tuple
    - Returns `string` with type (`'list'`, `'tuple'`, or `'single'`)
    '''
    if isinstance(item, list):
        return 'list'
    if isinstance(item, tuple):
        return 'tuple'
    return 'single'

def get_listuple_values(listuple) -> list:
    '''
    - `EXCEPTION-UNSAFE`
    - Recursively retrieves items from nested `lists` and `tuples`
    - Returns `list` of all retrieved values
    '''
    values = []
    if get_listuple_type(listuple) == 'single':
        values.append(listuple)
    else: # listuple is a list or tuple
        for item in listuple:
            if get_listuple_type(item) == 'single':
                values.append(item)
            else:
                values += get_listuple_values(item)
    return values

def log(file_path:str, text:str, date:bool=True, ts_args:list=[1,0,1,1,0]) -> int:
    '''
    - `EXCEPTION-UNSAFE`
    - Logs to `file_path` with timestamp
    - Creates file and its directory if nonexistent
    - `ts_args` is a list of arguments to pass to the timestamp
    - Returns
        - `0` if `file_path` had to be created
        - `1` if `file_path` already existed
    '''
    makedirs(parent(file_path))
    now = ''
    if date:
        t = ts_args
        now = timestamp(t[0], t[1], t[2], t[3], t[4]) + '  '
    exists = False
    if os.path.exists(file_path):
        exists = True
    orig_stdout = sys.stdout
    with open(file_path, 'a') as f:
        sys.stdout = f
        print(f'{now}{text}')
    sys.stdout = orig_stdout
    if exists:
        return 1
    return 0

def makedirs(*dirs) -> int:
    '''
    - `EXCEPTION-UNSAFE`
    - Creates directories for any passed values (must be full paths)
    - Input
        - `string`
        - Any nesting of `lists`/`tuples` with `string` elements
    - Returns
        - `int` of directories created
        - `-1` for input error
    '''
    count = 0
    if get_listuple_type(dirs) == 'tuple':
        for dir in get_listuple_values(dirs):
            if not os.path.exists(dir):
                os.makedirs(dir)
                count += 1
    else:
        return -1
    return count

def month2num(month_word:str) -> str:
    '''
    - `EXCEPTION-SAFE`
    - Converts month names to their 2-digit numerical equivalent
    - Returns
        - `string` with 2-digit number
        - empty `string` (`''`) if input is not a month
    '''
    months = ['january', 'february', 'march',
              'april', 'may', 'june',
              'july', 'august', 'september',
              'october', 'november', 'december']
    dict = {}
    for i, month in enumerate(months, 1):
        dict[month] = str(i).zfill(2)
    try:
        return dict[month_word.lower()]
    except KeyError:
        return ''

def parent(path:str='') -> str:
    '''
    - `EXCEPTION-UNSAFE`
    - Gets the parent path of something
    - Returns
        - parent path of `path` if provided
        - parent path of whatever file called `parent()`
    '''
    if path:
        if isinstance(path, str):
            return os.path.dirname(path)
        else:
            raise TypeError
    else:
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            try:
                host_path = os.path.realpath(__file__)
                return os.path.dirname(host_path)
            except NameError:
                return os.getcwd()

def remove(file_path:str, delete:bool=True) -> int:
    '''
    - `EXCEPTION-SAFE`
    - Deletes `file_path`
    - Returns
        - `1` for success
        - `0` for error
        - `-1` if `delete` is `False`
    '''
    if delete:
        if isinstance(delete, bool):
            try:
                os.remove(file_path)
                return 1
            except:
                return 0
    return -1

def sec_mod(seconds:float) -> list:
    '''
    - `EXCEPTION-SEMISAFE`
    - Formats `seconds` as `'04d16h47m04s'`
    - Returns `list` with `string` in given format and individual `int` values
    '''
    if not (isinstance(seconds, int) or isinstance(seconds, float)):
        raise TypeError
    if seconds < 0:
        return ['NegativeTime', 0, 0, 0, 0]
    elif 0 <= seconds < 1:
        return ['0s', 0, 0, 0, 0]
    result = ''
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        result += str(d).zfill(2) + 'd'
    if h:
        result += str(h).zfill(2) + 'h'
    if m:
        result += str(m).zfill(2) + 'm'
    if s:
        result += str(s).zfill(2) + 's'
    return [result, d, h, m, s]

def timestamp(brackets:bool=True, microseconds:bool=False, readable:bool=False, offset:bool=True, utc:bool=False) -> str:
    '''
    - `EXCEPTION-SEMISAFE`
    - Defaults to ISO format: `[2022-07-06T13:57:12-06:00]`
    - Returns `string` with current timestamp
    '''
    if utc:
        now = dt.utcnow()
        offset_val = '+00:00'
    else:
        now = dt.now()
        offset_val = str(now.astimezone())[-6:]
    if not microseconds:
        now = now.replace(microsecond=0)
    now = now.isoformat()
    if offset:
        now += offset_val
    if readable:
        now = now.replace('T', ' ')
        if offset:
            now = f'{now[:19]} {now[19:]}'
    if brackets:
        now = f'[{now}]'
    return now

def unzip(file:str, delete:bool=False) -> int:
    '''
    - `EXCEPTION-SEMISAFE`
    - Unzips archive files of type .7z, .gz, .rar, .tar, .zip
    - Returns `0` for success, `1` for delete failure,
        `2` for unzip failure, or `-1` if nothing was attempted
    '''
    from shutil import unpack_archive
    from py7zr import unpack_7zarchive

    fparent = parent(file)
    if file.endswith('.7z'):
        try:
            unpack_7zarchive(file, fparent)
            return remove(file, delete)
        except:
            return 2
    elif file.endswith(tuple(['.gz', '.rar', '.tar', '.zip'])):
        try:
            unpack_archive(file, fparent)
            return remove(file, delete)
        except:
            return 2
    else:
        return -1

def unzip_dir(dir:str) -> int:
    '''
    - `EXCEPTION-SEMISAFE`
    - Unzips all archives in a directory and repeats until it can't do more
        - Either no archives are left or the rest can't be unzipped
    - Returns `int` of unzipped archives
    '''
    unzipped = 0
    while True:
        unzipped_thisrun = 0
        for file in os.listdir(dir):
            status = unzip(f'{dir}\\{file}', delete=True)
            if status == 0:
                unzipped += 1
                unzipped_thisrun += 1
        if not unzipped_thisrun:
            break
    return unzipped

if __name__ == '__main__':
    print('oops! import this module instead')
    input('press enter to exit')

