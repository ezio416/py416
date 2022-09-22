import os
from pathlib import Path
from pprint import pprint
import sys

import pytest
from rich.traceback import install
install()

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')
import src.py416.files as p4f

def test_File():
    print(test_File.__name__)

    # dirs = []
    # files = []
    # for item in [f.File(file) for file in f.listdir('D:/test/test2')]:
    #     if item.isdir:
    #         dirs.append(item)
    #     else:
    #         files.append(item)

    # a = f.File('D:/test/a.txt')
    # print(a.name)
    # print('none')
    # a.rename('ickandballs.txt')
    # a.rename('fuckyou.csv').move('D:/test/d').delete()
    # a.move('D:/test/e')
    # a.move('D:/test/f')
    # a.move('C:/test')
    # a.rename('a.txt')
    # b = f.File('M:/test/b')
    # b.delete()
    # b.move('D:/test/c')
    # b.rename('c')
    # print(b.exists)
    # f.cd('M:/deciPush')
    # cdir = '\\\\bdi-az-data01\\Projects'
    # c = f.File(cdir)
    # d = f.File('.')
    # e = p4f.File('..')
    # h = f.File('M:/')

    # print('end test_File')
    pass

def test_cd():
    # a = p4f.cd('D:/test')
    # print(a)
    # b = p4f.cd('M:')
    # print(b)
    pass

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

def test_checkzip():
    pass

def test_copy():
    # d1 = 'D:/test/d1'
    # d2 = 'D:/test/d2'
    # f1 = 'D:/test/f1.txt'

    # a = p4f.copy(d1, d1, overwrite=True)
    # print(a)
    pass

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

def test_listdir():
    pass

def test_log():
    pass

def test_makedirs():
    pass

def test_move():
    pass

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

def test_rename():
    pass

def test_rmdir():
    pass

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

def test_unzip():
    pass

def test_unzipdir():
    pass

# test_File()
# test_cd()
# test_checkwindrive()
# test_checkzip()
# test_copy()
# test_forslash()
# test_getcwd()
# test_getpath()
# test_joinpath()
# test_listdir()
# test_log()
# test_move()
# test_parent()
# test_rename()
# test_rmdir()
# test_splitpath()
# test_unzip()
# test_unzipdir()