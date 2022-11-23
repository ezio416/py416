'''
| Author:  Ezio416
| Created: 2022-10-11
| Updated: 2022-11-23

- Functions for getting basic system information
'''
from datetime import datetime as dt
from json import dumps
import os
from platform import node, platform
from time import time
from typing import Union

from cpuinfo import get_cpu_info
import psutil as ps

from .general import secmod
from .variables import BYTE_G


def cpu(json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets info on the CPU

    Parameters
    ----------
    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: float | int | str)
        - arch: str
            - architecture (i.e. 'X86_64')
        - cores: int
            - number of physical cores (i.e. 12)
        - name: str
            - name (i.e. 'AMD Ryzen 9 3900X 12-Core Processor')
        - threads: int
            - number of logical/virtual cores (i.e. 24)
        - used_percent: float
            - current utilization percentage (i.e. 21.2)
            - unreliable as Python uses some overhead to run

    str
        - JSON string with all above info
    '''
    cpu_info = {}
    tmp = get_cpu_info()
    cpu_info['arch'] = tmp['arch']
    cpu_info['cores'] = ps.cpu_count(logical=False)
    cpu_info['name'] = tmp['brand_raw']
    cpu_info['threads'] = ps.cpu_count()
    cpu_info['used_percent'] = ps.cpu_percent(interval=0)
    if json:
        return dumps(cpu_info, indent=json_indent)
    return cpu_info


def disks(json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets disk usage on mapped drives on Windows (drives with a letter like C:)
    - all byte values are in GiB (1024^3 bytes)
    - returns empty dict if not on Windows

    Parameters
    ----------
    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: dict(str: float))
        - keys are drive letters (i.e. 'c')
        - drive: dict(str: float)
            - free: float
                - amount of free space left
            - total: float
                - total storage capacity
            - used: float
                - amount of space used
            - used_percent: float
                - percentage of space used

    str
        - JSON string with all above info
    '''
    disks = {}
    if os.name == 'nt':
        for let in 'abcdefghijklmnopqrstuvwxyz':
            try:
                psdu = ps.disk_usage(f'{let}:\\')
                disk_info = {}
                disk_info['free'] = round((psdu[2] / BYTE_G), 2)
                disk_info['total'] = round((psdu[0] / BYTE_G), 2)
                disk_info['used'] = round((psdu[1] / BYTE_G), 2)
                disk_info['used_percent'] = psdu[3]
                disks[let] = disk_info
            except Exception:
                pass
    if json:
        return dumps(disks, indent=json_indent)
    return disks


def full(now: float = 0, json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets all system info programmed into this module

    Parameters
    ----------
    now: float
        - Unix timestamp (presumably current time)
        - default: 0 (current time will be used)

    Parameters
    ----------
    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: dict)
        - keys are this module's function names (i.e. 'cpu')

    str
        - JSON string with all above info
    '''
    if not now:
        now = time()
    mydict = {}
    mydict['cpu'] = cpu()
    mydict['disks'] = disks()
    mydict['ram'] = ram()
    mydict['system'] = system(now)
    mydict['users'] = users(now)
    if json:
        return dumps(mydict, indent=json_indent)
    return mydict


def ram(json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets the RAM usage data
    - all byte values are in GiB (1024^3 bytes)

    Parameters
    ----------
    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: float)
        - free: float
            - amount of free space left
        - total: float
            - total storage capacity
        - used: float
            - amount of space used
        - used_percent: float
            - percentage of space used

    str
        - JSON string with all above info
    '''
    ram_info = {}
    psvm = ps.virtual_memory()
    ram_info['free'] = round((psvm[4] / BYTE_G), 2)
    ram_info['total'] = round((psvm[0] / BYTE_G), 2)
    ram_info['used'] = round((psvm[3] / BYTE_G), 2)
    ram_info['used_percent'] = psvm[2]
    if json:
        return dumps(ram_info, indent=json_indent)
    return ram_info


def system(now: float = 0, json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets various system info such as boot time

    Parameters
    ----------
    now: float
        - Unix timestamp (presumably current time)
        - default: 0 (current time will be used)

    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: float | str)
        - name: str
            - computer network name (i.e. 'Ezio-PC')
        - platform: str
            - operating system info (i.e. 'Windows-10-10.0.19044-SP0')
        - boot_time: float
            - system boot time in Unix time (i.e. 1665585199.3431532)
        - boot_time_nice: str
            - human-readable boot time (i.e. '2022-10-12 08:33:19 -06:00')
        - boot_uptime: float
            - number of seconds since boot (i.e. 11636.991024971008)
        - boot_uptime_nice: str
            - human-readable boot uptime (i.e. '03h13m56s')

    str
        - JSON string with all above info
    '''
    if not now:
        now = time()
    offset = str(dt.now().astimezone())[-6:]
    system_info = {}
    system_info['name'] = node()
    system_info['platform'] = platform()
    system_info['boot_time'] = ps.boot_time()
    system_info['boot_time_nice'] = f"{dt.fromtimestamp(system_info['boot_time']).strftime('%Y-%m-%d %H:%M:%S')} {offset}"
    system_info['boot_uptime'] = now - system_info['boot_time']
    system_info['boot_uptime_nice'] = secmod(system_info['boot_uptime'])[0]
    if json:
        return dumps(system_info, indent=json_indent)
    return system_info


def users(now: float = 0, json: bool = False, json_indent: int = 4) -> Union[dict, str]:
    '''
    - gets a list of users currently logged in

    Parameters
    ----------
    now: float
        - Unix timestamp (presumably current time)
        - default: 0 (current time will be used)

    json: bool
        - whether to return the output as a JSON string
        - default: false

    json_indent: int
        - indentation level for JSON output
        - default: 4

    Returns
    -------
    dict(str: dict(str: float|str))
        - keys are account names
        - user: dict(str: float|str))
            - login_time: float
                - user login time in Unix time (i.e. 1665585199.3431532))
            - login_time_nice: str
                - human-readable login time (i.e. '2022-10-12 08:33:19 -06:00')
            - login_uptime: float
                - number of seconds since login (i.e. 11636.991024971008)
            - login_uptime_nice: str
                - human-readable login uptime (i.e. '03h13m56s')

    '''
    if not now:
        now = time()
    offset = str(dt.now().astimezone())[-6:]
    users = {}
    user_list = ps.users()
    for i, z in enumerate(user_list):
        user_info = {}
        user_info['login_time'] = user_list[i][3]
        user_info['login_time_nice'] = f"{dt.fromtimestamp(user_info['login_time']).strftime('%Y-%m-%d %H:%M:%S')} {offset}"
        user_info['login_uptime'] = now - user_info['login_time']
        user_info['login_uptime_nice'] = secmod(user_info['login_uptime'])[0]
        users[user_list[i][0]] = user_info
    if json:
        return dumps(users, indent=json_indent)
    return users
