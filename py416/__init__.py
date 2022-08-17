'''
Name:    py416
Author:  Ezio416
Created: 2022
Updated: 2022-08-16
Version: 9.0

A collection of my custom-built functions
'''
from datetime import datetime as dt
import os
import sys

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