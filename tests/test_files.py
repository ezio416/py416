import os
from pathlib import Path
from pprint import pprint
import sys

import pytest
import pytest_check as check
from rich.traceback import install
install()

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')
import src.py416.files as p4f

# def test_File():
#     pass

def test_cd(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    tmp = p4f.cd(f'{str_path}/abc')
    check.equal(tmp, os.getcwd().replace('\\', '/'))

@pytest.mark.parametrize('i,o', [
    ('', ''),
    ('B', ''),
    ('C:', 'C:/'),
    ('D:/', 'D:/'),
    ('E://', ''),
    ('f:\\', 'F:/'),
    ('g;/', ''),
    ('h/', ''),
    ('I:/test', ''),
    ('/J', ''),
])
def test_checkwindrive(i, o):
    assert p4f.checkwindrive(i) == o

# def test_checkzip():
#     pass

# def test_copy():
#     pass

@pytest.mark.parametrize('i,o', [
    ('', ''),
    ('/', '/'),
    ('\\', '/'),
    ('D:\\test\\a\\b', 'D:/test/a/b'),
    ('\\\\bdi\\proj', '//bdi/proj'),
    ('/Users/Lance', '/Users/Lance'),
])
def test_forslash(i, o):
    assert p4f.forslash(i) == o

def test_getcwd():
    assert p4f.getcwd() == os.getcwd().replace('\\', '/')

@pytest.mark.parametrize('i,o', [
    # Unix
    ('/', '/'),
    ('/.', '/'),
    ('/..', '/'),
    ('/gfsyt/trw', '/gfsyt/trw'),
    ('/dir1/dir2/.', '/dir1/dir2'),
    ('/dir1/dir2/..', '/dir1'),
    #Windows
    ('D:', 'D:/'),
    ('D:/', 'D:/'),
    ('D:/test/party/time/baby', 'D:/test/party/time/baby'),
    ('D:/test/a/.', 'D:/test/a'),
    ('D:/test/a/..', 'D:/test'),
    ('//', '//'),
    ('\\\\bdi-az-data01', '//bdi-az-data01'),
    ('\\\\bdi-az-data01\\Projects', '//bdi-az-data01/Projects'),
    ('//bdi-az-data01/Projects/.', '//bdi-az-data01/Projects'),
    ('//bdi-az-data01/Projects/..', '//bdi-az-data01'),
    # None
    ('', ''),
    ('folder/..', ''),
])
def test_getpath(i, o):
    assert p4f.getpath(i) == o

@pytest.mark.parametrize('i,o', [
    # Unix
    ('/', '/'),
    (('/', 'abc', 'def', 'ghi.txt'), '/abc/def/ghi.txt'),
    ('/Users', '/Users'),
    (('/Users/lance', 'docs', 'f1/f2'), '/Users/lance/docs/f1/f2'),
    ('/mnt/folder/.', '/mnt/folder'),
    ('/mnt/folder/..', '/mnt'),
    (('/mnt', 'folder/.'), '/mnt/folder'),
    (('/mnt', 'folder/..'), '/mnt'),
    (('/mnt', ''), '/mnt'),
    # Windows
    ('T:', 'T:/'),
    ('D:/', 'D:/'),
    (('G:', 'godaddy'), 'G:/godaddy'),
    (((['D:/', 'Windows', 'system32']), ['deleteme']), 'D:/Windows/system32/deleteme'),
    ('C:/same/.', 'C:/same'),
    ('C:/up/a/..', 'C:/up'),
    (('C:/', 'same/.'), 'C:/same'),
    (('C:/', 'up/..'), 'C:/'),
    (('C:/', 'up/a/..'), 'C:/up'),
    ('//', '//'),
    ('//bdi', '//bdi'),
    (('//bdi', 'drive'), '//bdi/drive'),
    # None
    ('', ''),
    (('', ''), ''),
    ('J', 'J'),
    (('alpha', 'bet'), 'alpha/bet'),
])
def test_joinpath(i, o):
    assert p4f.joinpath(i) == o

def test_listdir(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    d1 = f'{str_path}/testdir'
    f1 = f'{str_path}/file.txt'
    f2 = f'{d1}/file2.txt'
    check.equal(p4f.listdir(str_path), ())
    os.makedirs(d1)
    check.equal(p4f.listdir(str_path), (d1,))
    with open(f1, 'a') as f:
        f.write('this is file number 1')
    with open(f2, 'a') as f:
        f.write('this is file number 2')
    check.is_in(d1, p4f.listdir(str_path))
    check.is_in(d1, p4f.listdir(str_path, files=False))
    check.is_in(f1, p4f.listdir(str_path))
    check.is_in(f1, p4f.listdir(str_path, dirs=False))
    check.is_in(f2, p4f.listdir(d1))
    check.is_in(f2, p4f.listdir(d1, dirs=False))

# def test_log():
#     pass

def test_makefile(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    fname = 'test.txt'
    fpath = f'{str_path}/{fname}'
    p4f.makefile(fpath, 'message')
    check.equal(os.listdir(str_path), [fname])
    with open(fpath, 'r') as file:
        tmp = file.read()
    check.equal(tmp, 'message')
    try:
        p4f.makefile(fpath, 'message2')
        raise Exception('that should\'ve failed')
    except FileExistsError:
        pass
    p4f.makefile(fpath, 'message3', overwrite=True)
    with open(fpath, 'r') as file:
        tmp3 = file.read()
    check.equal(tmp3, 'message3')
    p4f.makefile(fpath, overwrite=True)
    with open(fpath, 'r') as file:
        tmp3 = file.read()
    check.equal(tmp3, '')    

def test_makedirs(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    dirs = ['abc', 'def', ('ghi', ['jkl'])], ('mno', ('pqr')), [[['stu/sub'], ['vwx/sub/sub']], ('yz/a/b/c/d/e/f/g',)]
    os.chdir(str_path)
    bad = p4f.makedirs(dirs)
    tmp = os.listdir()
    tmp.sort()
    check.equal(tmp, ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vwx', 'yz'])
    os.chdir('stu/sub')
    os.chdir('../..')
    os.chdir('vwx/sub/sub')
    os.chdir('../../..')
    os.chdir('yz/a/b/c/d/e/f/g')

# def test_move():
#     pass

@pytest.mark.parametrize('i,o', [
    # Unix
    ('/', '/'),
    ('/.', '/'),
    ('/..', '/'),
    ('/gfsyt/trw', '/gfsyt'),
    ('/dir1/dir2/.', '/dir1'),
    ('/dir1/dir2/..', '/'),
    # Windows
    ('D:', 'D:/'),
    ('D:/', 'D:/'),
    ('D:/test/party/time/baby', 'D:/test/party/time'),
    ('D:/test/a/.', 'D:/test'),
    ('D:/test/a/..', 'D:/'),
    ('//', '//'),
    ('\\\\bdi-az-data01', '//bdi-az-data01'),
    ('\\\\bdi-az-data01\\Projects', '//bdi-az-data01'),
    ('//bdi-az-data01/Projects/.', '//bdi-az-data01'),
    ('//bdi-az-data01/Projects/..', '//bdi-az-data01'),
    # None
    ('', ''),
    ('folder/..', ''),
])
def test_parent(i, o):
    assert p4f.parent(i) == o

# def test_rename(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
    
# def test_rmdir():
#     pass

@pytest.mark.parametrize('i,o', [
    # Unix
    ('/', ('/',)),
    ('/.', ('/',)),
    ('/..', ('/',)),
    ('/gfsyt/trw', ('/', 'gfsyt', 'trw')),
    ('/dir1/dir2/.', ('/', 'dir1', 'dir2')),
    ('/dir1/dir2/..', ('/', 'dir1')),
    # Windows
    ('D:', ('D:/',)),
    ('D:/', ('D:/',)),
    ('D:/test/party/time/baby', ('D:/', 'test', 'party', 'time', 'baby')),
    ('D:/test/a/.', ('D:/', 'test', 'a')),
    ('D:/test/a/..', ('D:/', 'test')),
    ('//', ('//',)),
    ('\\\\bdi-az-data01', ('//bdi-az-data01',)),
    ('\\\\bdi-az-data01\\Projects', ('//bdi-az-data01', 'Projects')),
    ('//bdi-az-data01/Projects/.', ('//bdi-az-data01', 'Projects')),
    ('//bdi-az-data01/Projects/..', ('//bdi-az-data01',)),
    # None
    ('', ('',)),
    ('folder/..', ('',))
])
def test_splitpath(i, o):
    assert p4f.splitpath(i) == o

# def test_unzip():
#     pass

# def test_unzipdir():
#     pass
