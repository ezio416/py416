'''
| Author:  Ezio416
| Created: 2022-08-18
| Updated: 2022-09-26

- Functions for various things
- These are all imported to py416 directly, so just call them like: :func:`py416.gettype(object)`
'''
from datetime import datetime as dt


def gettype(thing) -> str:
    '''
    - gets the type of an object
    - wraps `type() <https://docs.python.org/3/library/functions.html#type>`_
    
    Parameters
    ----------
    thing
        - object of any type
    
    Returns
    -------
    str
        - type of object
    '''
    return str(type(thing)).split("'")[1]


def month2num(month_word: str) -> str:
    '''
    - converts month names to their 2-digit number
    
    Parameters
    ----------
    month_word: str
        - full month name
    
    Returns
    -------
    str
        - zero-padded 2-digit number
    '''
    if gettype(month_word) != 'str':
        raise TypeError(f'input must be a string; invalid: {month_word}')
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december']
    mydict = {}
    for i, month in enumerate(month_list, 1):
        mydict[month] = str(i).zfill(2)
    try:
        return mydict[month_word.lower()]
    except KeyError:
        return ''


def secmod(seconds: float, sep: str = '') -> tuple:
    '''
    - formats a number of seconds nicely, split by days, hours, minutes, and seconds
    - takes the absolute value of the input so the result is always positive
    
    Parameters
    ----------
    seconds: int | float
        - number to convert
    sep: str
        - separator between values
        - default: nothing
    
    Returns
    -------
    tuple [str | int]
        - string in format and individual values
        - i.e. ('04d16h47m09s', 9, 47, 16, 4)
    '''
    seconds = abs(int(seconds))
    if gettype(sep) != 'str':
        raise ValueError(f'input must be a string; invalid: {sep}')
    if not seconds:
        return ['0s', 0, 0, 0, 0]
    result = ''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    def zf(var): return str(var).zfill(2)
    if d:
        result += zf(d) + 'd' + sep
    if h:
        result += zf(h) + 'h' + sep
    if m:
        result += zf(m) + 'm' + sep
    if s:
        result += zf(s) + 's'
    result = result.rstrip(sep)
    return result, s, m, h, d


def timestamp(brackets: bool = True, micro: bool = False, offset: bool = True, readable: bool = False, seconds: bool = True, utc: bool = False) -> str:
    '''
    - creates a timestamp in ISO format with additional formatting
    - default example: [2022-07-06T13:57:12-06:00]
    
    Parameters
    ----------
    brackets: bool
        - whether to surround timestamp in square brackets
        - default: True
    micro: bool
        - whether to include microseconds
        - default: False
    offset: bool
        - whether to include offset from UTC, e.g. timezone
        - default: True
    readable: bool
        - whether to internal whitespace for legibility
        - default: False
    seconds: bool
        - whether to include seconds
        - default: True
    utc: bool
        - current UTC time
        - default: False
    
    Returns
    -------
    str
        - current timestamp with chosen formatting
        - i.e. [2022-08-18 07:15:43.962 +00:00]
    '''
    brackets, micro, offset, readable, seconds, utc = (bool(flag) for flag in (brackets, micro, offset, readable, seconds, utc))
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


def unpack(iterable) -> tuple:
    '''
    - recursively retrieves items from some iterable types
    
    Parameters
    ----------
    iterable: list | tuple
        - thing to unpack
    
    Returns
    -------
    tuple
        - all retrieved items
    `iterable` itself if not a list or tuple
    '''
    iterables = ('list', 'tuple')
    if gettype(iterable) not in iterables:
        return iterable
    values = []
    for item in iterable:
        if gettype(item) not in iterables:
            values.append(item)
        else:
            values += list(unpack(item))
    return tuple(values)
