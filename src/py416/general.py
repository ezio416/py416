'''
Name:    py416.general
Author:  Ezio416
Created: 2022-08-18
Updated: 2022-08-19

Methods for various things
'''
from datetime import datetime as dt

def gettype(thing) -> str:
    '''
    - Wrapper for `type()`
    - Gets the type of an object
    - Input: `thing`: object of any type
    - Return: `str` with type
    '''
    return str(type(thing)).split("'")[1]

def month2num(month_word:str) -> str:
    '''
    - Converts month names to their 2-digit number
    - Input: `month_word` (`str`): full month name
    - Return: `str` with zero-padded 2-digit number
    '''
    if gettype(month_word) != 'str':
        raise TypeError('Input must be a string')
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december']
    mydict = {}
    for i, month in enumerate(month_list, 1):
        mydict[month] = str(i).zfill(2)
    return mydict[month_word.lower()]

def sec_mod(seconds:float, sep:str='') -> list:
    '''
    - Formats a number of seconds nicely, split by days, hours, minutes, and seconds
        - i.e. `'04d16h47m09s'`
    - Takes the absolute value of input, so 
    - Input:
        - `seconds`: `int` or `float`
        - `sep` (`str`): separator between values
            - Default: no separator
    - Return:
        - `list` with `str` in given format and `int` values
            - i.e. `['04d16h47m09s', 9, 47, 16, 4]`
    '''
    seconds = abs(int(seconds))
    if gettype(sep) != 'str':
        raise ValueError('Input must be a string')
    if not seconds:
        return ['0s', 0, 0, 0, 0]
    result = ''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    zf = lambda var: str(var).zfill(2)
    if d:
        result += zf(d) + 'd' + sep
    if h:
        result += zf(h) + 'h' + sep
    if m:
        result += zf(m) + 'm' + sep
    if s:
        result += zf(s) + 's'
    if result.endswith(sep):
        result = result.replace(sep, '')
    return [result, s, m, h, d]

def timestamp(brackets:bool=True, micro:bool=False, offset:bool=True, readable:bool=False, seconds:bool=True, utc:bool=False) -> str:
    '''
    - Creates a timestamp in ISO format with additional formatting
        - Default example: [2022-07-06T13:57:12-06:00]
    - Input (`bool`):
        - `brackets`: surround timestamp in square brackets
            - Default: `True`
        - `micro`: include microseconds
            - Default: `False`
        - `offset`: include offset from UTC, e.g. timezone
            - Default: `True`
        - `readable`: internal whitespace for legibility
            - Default: `False`
        - `seconds`: include seconds
            - Default: `True`
        - `utc`: current UTC time
            - Default: `False`
    - Return:
        - `str` with current timestamp with chosen formatting
            - i.e. `[2022-08-18 07:15:43.962 +00:00]`
    '''
    if utc:
        now = dt.utcnow()
        offset_val = '+00:00'
    else:
        now = dt.now()
        offset_val = str(now.astimezone())[-6:]
    if not micro:
        now = now.replace(microsecond=0)
    now = now.isoformat()
    if not seconds:
        now = now[:-3]
    if readable:
        now = now.replace('T', ' ')
        if offset:
            now += ' '
    if offset:
        now += offset_val
    if brackets:
        now = f'[{now}]'
    return now.strip()

def unpack(iterable) -> list:
    '''
    - Recursively retrieves items from nested `list` and `tuple` types
    - Input: `iterable`: `list`/`tuple`
    - Return:
        - `list` of all retrieved items
        - `iterable` itself if not a `list`/`tuple`
    '''
    iterable_list = ['list', 'tuple']
    if gettype(iterable) not in iterable_list:
        return iterable
    else:
        values = []
        for item in iterable:
            if gettype(item) not in iterable_list:
                values.append(item)
            else:
                values += unpack(item)
    return values

