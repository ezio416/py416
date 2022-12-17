'''
| Author:  Ezio416
| Created: 2022-08-18
| Updated: 2022-11-21

- Functions for various things
- These are all imported to py416 directly, so just call them like so: :func:`py416.timestamp`
'''
from datetime import datetime as dt
from email.message import EmailMessage
from inspect import currentframe
from re import findall
from smtplib import SMTP_SSL
from ssl import create_default_context

from .variables import SEC_D, SEC_H, SEC_M


def bytesize(byte: int, si: bool = False) -> str:
    '''
    - scales a number of bytes to a prefixed format

    Parameters
    ----------
    byte: int
        - number of bytes to scale

    si: bool
        - whether to use SI units (1000^x bytes: KB, MB, GB)
        - default: False (1024^x bytes: KiB, MiB, GiB)

    Returns
    -------
    str
        - bytes in prefixed format, rounded to 2 decimal places
        - i.e.:
            - 1200000 => '1.20MB'
            - 1253656678 => '1.17GiB'
    '''
    byte = int(byte)
    if byte < 0:
        raise ValueError(f'bytes can\'t be negative; invalid: {byte}')
    if si:
        factor = 1000
        units = ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    else:
        factor = 1024
        units = ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi')
    if byte < factor:  # less than 1000 or 1024 bytes
        return f'{byte}B'
    for unit in units:
        if byte < factor:
            return f'{byte:.2f}{unit}B'
        byte /= factor
    return f'{byte*factor:.2f}{unit}B'  # user passed in stupidly large number


def emailsmtp(sender_email: str, recipient: str, subject: str, body: str, smtp_server: str, smtp_port: int, password: str, sender_name: str = '') -> bool:
    '''
    - sends an email via SMTP

    Parameters
    ----------
    sender_email: str
        - email address to send from

    recipient: str
        - email address to send to

    subject: str
        - text to put in the email subject

    body: str
        - test to put in the email body

    smtp_server: str
        - host name for SMTP server

    smtp_port: int
        - port for SMTP server

    password: str
        - password for sender email

    sender_name: str
        - name to show in the 'from' field
        - default: none

    Returns
    -------
    bool
        - whether send was successful
    '''
    msg = EmailMessage()
    if sender_name:
        msg['From'] = f'{sender_name} <{sender_email}>'
    else:
        msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with SMTP_SSL(host=smtp_server, port=smtp_port, context=create_default_context()) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        return True
    except Exception:
        return False


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


def lineno() -> int:
    '''
    - gets the line number in the file where the function was called from

    Returns
    -------
    int
        - line number in Python script
    '''
    return currentframe().f_back.f_lineno


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
    if type(month_word) is not str:
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


def pprint(iterable: object, do_print: bool = True, level: int = 0) -> str:
    '''
    - pretty print an iterable object without splitting strings
    - not yet working for dictionaries or special iterable types

    Parameters
    ----------
    iterable: object
        - thing to pretty print

    do_print: bool
        - whether to print the output
        - default: True

    level: int
        - recursion level
        - not meant to be changed (not useful to the user anyway)

    Returns
    -------
    str
        - output
    '''
    output = ' ' * level
    if (typ := type(iterable)) not in (list, set, tuple):
        return output + (f"'{iterable}'" if typ is str else str(iterable))
    if typ is list:
        open, close = '[', ']'
    elif typ is set:
        open, close = '{', '}'
    elif typ is tuple:
        open, close = '(', ')'
    output += open
    for i, item in enumerate(iterable):
        output += pprint(item, do_print=False, level=(level + 1 if i else 0)) + ',\n'
    output = output.rstrip(',\n') + close
    if do_print:
        print(output)
    return output


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
    if type(sep) is not str:
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


def secmod_inverse(timestr: str) -> int:
    '''
    - does essentially the opposite of :func::`secmod`
    - converts a string to a number of seconds

    Parameters
    ----------
    timestr: str
        - representation of time
        - must be formatted like the base output from :func::`secmod`, i.e. "3d16h5m47s"
        - can be missing parts, i.e. "3s47s"
        - capitalization is ignored
        - if multiple of the same type of value are passed in the string, i.e. "4h16h", only the first value is grabbed

    Returns
    -------
    int
        - number of seconds
    '''
    if type(timestr) is not str:
        raise TypeError(f'input must be a string; invalid: {timestr}')
    timestr = timestr.lower()
    dy = findall(r'[\d]{1,}[d]{1}', timestr)
    dy = int(dy[0].split('d')[0]) if dy else 0
    hr = findall(r'[\d]{1,}[h]{1}', timestr)
    hr = int(hr[0].split('h')[0]) if hr else 0
    mn = findall(r'[\d]{1,}[m]{1}', timestr)
    mn = int(mn[0].split('m')[0]) if mn else 0
    sc = findall(r'[\d]{1,}[s]{1}', timestr)
    sc = int(sc[0].split('s')[0]) if sc else 0
    return dy * SEC_D + hr * SEC_H + mn * SEC_M + sc


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
        - if `iterable` is not actually iterable, returns a tuple with just the item
    '''
    iterables = (list, tuple)
    if type(iterable) not in iterables:
        return iterable,
    values = []
    for item in iterable:
        if type(item) not in iterables:
            values.append(item)
        else:
            values += list(unpack(item))
    return tuple(values)
