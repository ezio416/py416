import os
from pathlib import Path
from pprint import pprint
import sys

import pytest
import pytest_check as check
from rich.traceback import install
install()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.py416.files as p4f

# def test_File(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

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

# def test_checkzip(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

def test_copy(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    dname = 'dir'
    dname2 = 'dir2'
    dpath = f'{str_path}/{dname}'
    fname = 'file.txt'
    fpath = f'{str_path}/{fname}'
    msg = 'message'
    msg2 = '\nmore text'
    os.makedirs(dpath)
    with open(fpath, 'a') as file:
        file.write(msg)
    p4f.copy(fpath, dpath)  # copy file
    with open(f'{dpath}/{fname}') as file:
        tmp = file.read()
    check.equal(tmp, msg)
    p4f.copy(dpath, dname2)  # copy dir
    os.chdir(f'{dname2}/{dname}')
    check.equal(os.listdir(), [fname])
    os.chdir(str_path)
    with open(fpath, 'a') as file:
        file.write(msg2)
    p4f.copy(fpath, dpath, overwrite=True)  # overwrite file
    with open(f'{dpath}/{fname}') as file:
        tmp = file.read()
    check.equal(tmp, f'{msg}{msg2}')
    p4f.copy(dpath, dname2, overwrite=True)  # overwrite dir
    with open(f'{dname2}/{dname}/{fname}') as file:
        tmp = file.read()
    check.equal(tmp, f'{msg}{msg2}')

# def test_delete(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

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
    tmp = p4f.listdir(str_path, recursive=True)
    check.is_in(d1, tmp)
    check.is_in(f1, tmp)
    check.is_in(f2, tmp)

def test_listdir_search(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    os.chdir(str_path)
    dirs = 'a', 'b/1', 'c/1/2', 'd/1/2/3', 'e/1/2/3/a', 'f/1/2/3/b', 'g/1/2/3/c'
    files = []
    files2 = []
    for i, dir in enumerate(dirs):
        os.makedirs(dir)
        files.append(f'{str_path}/{dir}/file{i}.txt')
        files2.append(f'{str_path}/{dir}/letter{i}.txt')
    for i, file in enumerate(files):
        with open(file, 'a') as f:
            f.write(f'msg {i}')
    for i, file in enumerate(files2):
        with open(file, 'a') as f:
            f.write(f'msg {i}')
    tree = p4f.listdir(recursive=True, search='*')
    for file in files:
        check.is_in(file, tree)
    for file in files2:
        check.is_in(file, tree)
    tree = p4f.listdir(recursive=True, search='f*')
    for file in files:
        check.is_in(file, tree)
    for file in files2:
        check.is_not_in(file, tree)
    tree = p4f.listdir(recursive=True, search='l*')
    for file in files:
        check.is_not_in(file, tree)
    for file in files2:
        check.is_in(file, tree)
    tree = p4f.listdir(recursive=True, search='*le*')
    for file in files:
        check.is_in(file, tree)
    for file in files2:
        check.is_in(file, tree)

# def test_listdir_recency(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

# def test_log(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

def test_makedirs(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    dirs = ['abc', 'def', ('ghi', ['jkl'])], ('mno', ('pqr')), [[['stu/sub'], ['vwx/sub/sub']], ('yz/a/b/c/d/e/f/g',)]
    os.chdir(str_path)
    bad = p4f.makedirs(dirs)
    check.equal(bad, ())
    tmp = os.listdir()
    tmp.sort()
    check.equal(tmp, ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vwx', 'yz'])
    os.chdir('stu/sub')
    os.chdir('../..')
    os.chdir('vwx/sub/sub')
    os.chdir('../../..')
    os.chdir('yz/a/b/c/d/e/f/g')

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

def test_move(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    os.chdir(str_path)
    dname = 'dir'
    dname2 = 'dir2'
    fname = 'file.txt'
    msg = 'message'
    msg2 = '\nmore text'
    with open(fname, 'a') as file:
        file.write(msg)
    tmp = os.listdir()
    check.is_not_in(dname, tmp)
    check.is_in(fname, tmp)
    p4f.move(fname, dname)  # move file
    tmp = os.listdir()
    check.is_not_in(fname, tmp)
    tmp = os.listdir(dname)
    check.is_in(fname, tmp)
    with open(fname, 'a') as file:
        file.write(msg2)
    p4f.move(fname, dname, overwrite=True)  # overwrite file
    tmp = os.listdir()
    check.is_not_in(fname, tmp)
    with open(f'{dname}/{fname}', 'r') as file:
        tmp = file.read()
    check.equal(tmp, msg2)
    p4f.move(dname, dname2)  # move dir
    tmp = os.listdir()
    check.is_in(dname2, tmp)
    check.is_not_in(dname, tmp)
    check.is_in(dname, os.listdir(dname2))
    os.makedirs(dname)
    with open(f'{dname}/{fname}', 'a') as file:
        file.write(msg)
    p4f.move(dname, dname2, overwrite=True)  # overwrite dir
    tmp = os.listdir()
    check.is_not_in(dname, tmp)
    with open(f'{dname2}/{dname}/{fname}', 'r') as file:
        tmp = file.read()
    check.equal(tmp, msg)

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

def test_rename(tmp_path):
    str_path = str(tmp_path).replace('\\', '/')
    os.chdir(str_path)
    dname = 'dir'
    dname2 = 'anotherdir'
    fname = 'file.txt'
    fname2 = 'somefile.csv'
    msg = 'message'
    os.makedirs(dname)
    with open(fname, 'a') as file:
        file.write(msg)
    tmp = os.listdir()
    check.is_in(dname, tmp)
    check.is_not_in(dname2, tmp)
    check.is_in(fname, tmp)
    check.is_not_in(fname2, tmp)
    p4f.rename(dname, dname2)
    p4f.rename(fname, fname2)
    tmp = os.listdir()
    check.is_in(dname2, tmp)
    check.is_not_in(dname, tmp)
    check.is_in(fname2, tmp)
    check.is_not_in(fname, tmp)

# def test_rmdir(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

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

# def test_unzip(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)

# def test_unzipdir(tmp_path):
#     str_path = str(tmp_path).replace('\\', '/')
#     os.chdir(str_path)
