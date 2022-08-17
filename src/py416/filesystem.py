'''
Name:    py416.filesystem
Author:  Ezio416
Created: 2022-08-16
Updated: 2022-08-16
Version: 1.0

Methods for file system manipulation
'''
import os
import shutil as sh

def cd(dir:str='..') -> bool:
    '''
    - `EXCEPTION-SAFE`
    - Change current working directory to `dir`
    - Defaults to going up a directory
    - Returns
        - `True` for success
        - `False` for error
    '''
    try:
        os.chdir(dir)
        return True
    except:
        return False

