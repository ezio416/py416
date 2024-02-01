import os
import sys
import time

import pytest
import pytest_check as check

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.py416.files as p4f
import src.py416.variables as p4v

# def test_File(tmp_path):
#     os.chdir(str_path := str(tmp_path).replace('\\', '/'))

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
#     os.chdir(str_path := str(tmp_path).replace('\\', '/'))

def test_copy(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
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

def test_delete(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    nums = 1, 2, 3, 4, 5
    dirs = [f'{str_path}/dir{a}/subdir{b}' for a in nums for b in nums]
    for dir in dirs:
        os.makedirs(dir)
        if '/dir3/' in dir:
            with open(file := f'{dir}/file', 'a') as f:
                f.write(f'I am {file}')
    [p4f.delete(dir) for dir in os.listdir()]
    check.equal(os.listdir(), ['dir3'])
    [p4f.delete(dir, force=True) for dir in os.listdir()]
    check.equal(os.listdir(), [])
    for dir in dirs:
        os.makedirs(dir)
        if '/dir3/' in dir:
            with open(file := f'{dir}/file', 'a') as f:
                f.write(f'I am {file}')
    with open('file', 'a') as f:
        f.write(f'base file')
    [p4f.delete(item) for item in os.listdir()]
    check.equal(os.listdir(), ['dir3'])

def test_delete_trash(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    nums = 1, 2, 3, 4, 5
    dirs = [f'{str_path}/dir{a}/subdir{b}' for a in nums for b in nums]
    for dir in dirs:
        os.makedirs(dir)
        if '/dir3/' in dir:
            with open(file := f'{dir}/file', 'a') as f:
                f.write(f'I am {file}')
    [p4f.delete(dir, trash=True) for dir in os.listdir()]
    check.equal(os.listdir(), [])

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
    # Windows
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
    # Any
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
    # Any
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
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
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

def test_listdir_recency(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    files = []
    nums = 1, 2, 3, 4, 5
    dirs = (f'{str_path}/dir{num}' for num in nums)
    now = time.time()
    for dir in dirs:
        os.makedirs(dir)
        files += [f'{dir}/file{num}' for num in nums]
    for file in files:
        with open(file, 'a') as f:
            f.write(f'my name is {file}')
        if '/dir1/' in file or '/file1' in file:  # 1970
            os.utime(file, (1, 1))
        if '/dir2/' in file or '/file2' in file:  # 40 years ago
            os.utime(file, tuple([now - 1_262_304_000] * 2))
        if '/file3' in file:  # a billion seconds ago
            os.utime(file, (now - 1e9, now - 1e9))
        if '/dir4/' in file:  # an hour ago
            os.utime(file, (now - 3600, now - 3600))
    tmp = p4f.listdir(dirs=False, recursive=True)  # all files
    check.equal(len(tmp), 25)
    (check.is_in(file, tmp) for file in files)

    tmp = p4f.listdir(dirs=False, recursive=True, recency=1e3)  # files for which we didn't change the modify date
    check.equal(len(tmp), 4)
    files_unmodified = [f'{str_path}/dir{a}/file{b}' for a in (3, 5) for b in (4, 5)]
    (check.is_in(file, tmp) for file in files_unmodified)

    tmp = p4f.listdir(dirs=False, recursive=True, recency=4000)  # including an hour
    check.equal(len(tmp), 9)
    files_hour = files_unmodified + [f'{str_path}/dir4/file{num}' for num in nums]
    (check.is_in(file, tmp) for file in files_hour)

    tmp = p4f.listdir(dirs=False, recursive=True, recency='11575d')  # including a billion seconds
    check.equal(len(tmp), 13)
    files_2001 = files_hour + [f'{str_path}/dir{num}/file3' for num in (1, 2, 3, 5)]
    (check.is_in(file, tmp) for file in files_2001)

    tmp = p4f.listdir(dirs=False, recursive=True, recency='15000d17h3m59s')  # including 40 years
    check.equal(len(tmp), 20)
    files_40years = files_2001 + [f'{str_path}/dir2/file{b}' for b in (1, 2, 4, 5)] + [f'{str_path}/dir{a}/file2' for a in (1, 3, 5)]
    (check.is_in(file, tmp) for file in files_40years)

    tmp = p4f.listdir(dirs=False, recursive=True, recency=2e9)  # including 1970 (should now be all)
    check.equal(len(tmp), 25)
    files_1970 = files_40years + [f'{str_path}/dir1/file{b}' for b in (1, 4, 5)] + [f'{str_path}/dir{a}/file1' for a in (3, 5)]
    (check.is_in(file, tmp) for file in files_1970)

def test_listdir_dict(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    files = []
    nums = 1, 2, 3, 4, 5
    dirs = (f'{str_path}/dir{num}' for num in nums)
    now = time.time()
    for dir in dirs:
        os.makedirs(dir)
        files += [f'{dir}/file{num}' for num in nums]
    for file in files:
        with open(file, 'a') as f:
            f.write(f'my name is {file}')
        if '/dir1/' in file or '/file1' in file:  # 1970
            os.utime(file, (1, 1))
        if '/dir2/' in file or '/file2' in file:  # 40 years ago
            os.utime(file, tuple([now - 1_262_304_000] * 2))
        if '/file3' in file:  # a billion seconds ago
            os.utime(file, (now - 1e9, now - 1e9))
        if '/dir4/' in file:  # an hour ago
            os.utime(file, (now - 3600, now - 3600))

    tmp = p4f.listdir(recursive=True, return_dict=True)
    check.is_(type(tmp), dict)
    check.equal(len(tmp), 30)
    (check.is_in(file, tmp) for file in files)

# def test_log(tmp_path):
#     os.chdir(str_path := str(tmp_path).replace('\\', '/'))

def test_makedirs(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    dirs = ['abc', 'def', ('ghi', ['jkl'])], ('mno', ('pqr')), [[['stu/sub'], ['vwx/sub/sub']], ('yz/a/b/c/d/e/f/g',)]
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
    with open(fpath, 'r', encoding='utf-8') as file:
        tmp = file.read()
    check.equal(tmp, 'message')
    try:
        p4f.makefile(fpath, 'message2')
        raise Exception('that should\'ve failed')
    except FileExistsError:
        pass
    p4f.makefile(fpath, 'message3', overwrite=True)
    with open(fpath, 'r', encoding='utf-8') as file:
        tmp3 = file.read()
    check.equal(tmp3, 'message3')
    p4f.makefile(fpath, overwrite=True)
    with open(fpath, 'r', encoding='utf-8') as file:
        tmp3 = file.read()
    check.equal(tmp3, '')

def test_move(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
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
    # Any
    ('', ''),
    ('folder/..', ''),
])
def test_parent(i, o):
    assert p4f.parent(i) == o

def test_parent_default(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    assert p4f.parent() == os.path.dirname(os.getcwd()).replace('\\', '/')

def test_readfile(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    file = 'file.txt'
    msg = 'some text\nin here'
    with open(file, 'a') as f:
        f.write(msg)
    read = p4f.readfile(file)
    check.equal(read, msg)

def test_rename(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
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

def test_rmdir(tmp_path):
    os.chdir(str_path := str(tmp_path).replace('\\', '/'))
    nums = 1, 2, 3, 4, 5
    [os.makedirs(f'dir{a}/subdir{b}') for a in nums for b in nums]
    for file in (f'dir{a}/file{b}' for a in (1, 3) for b in (1, 2, 3)):
        with open(file, 'a') as f:
            f.write(f'i am {file}')
    for file in (f'dir{a}/subdir{b}/subfile{c}' for a in (2, 4) for b in (1, 4, 5) for c in (1, 2, 3, 4, 5)):
        with open(file, 'a') as f:
            f.write(f'i am {file}')
    check.equal(p4f.rmdir('dir1'), 5)
    check.equal(p4f.rmdir('dir2'), 2)
    check.equal(p4f.rmdir('dir3'), 5)
    check.equal(p4f.rmdir('dir4'), 2)
    check.equal(p4f.rmdir('dir5', delroot=True), 6)
    [os.makedirs(dir) for a in nums for b in nums if not os.path.exists(dir := f'dir{a}/subdir{b}')]
    check.equal(p4f.rmdir('.', delroot=True), 20)

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
    # Any
    ('', ('',)),
    ('folder/..', ('',))
])
def test_splitpath(i, o):
    assert p4f.splitpath(i) == o

# def test_unzip(tmp_path):
#     os.chdir(str_path := str(tmp_path).replace('\\', '/'))

# def test_unzipdir(tmp_path):
#     os.chdir(str_path := str(tmp_path).replace('\\', '/'))


# from datetime import datetime as dt
# now = str(dt.now()).split('.')[0].replace(' ', '__').replace(':', '-')
# p4f.makedirs(dir := f'D:/pytest-temp/{now}')
# test_delete_trash(dir)
