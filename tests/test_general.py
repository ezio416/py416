import os
import sys

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')

import src.py416.general as g
from src.py416.files import File

def test_gettype():
    assert g.gettype(True)  == 'bool'
    assert g.gettype(False) == 'bool'
    
    assert g.gettype(bytes())         == 'bytes'
    assert g.gettype(b'')             == 'bytes'
    assert g.gettype(b'hello')        == 'bytes'
    assert g.gettype(b'\xE2\x82\xAC') == 'bytes'
    
    assert g.gettype(bytearray()) == 'bytearray'
    
    assert g.gettype(complex()) == 'complex'
    
    assert g.gettype(dict())                   == 'dict'
    assert g.gettype({})                       == 'dict'
    assert g.gettype({1: 2})                   == 'dict'
    assert g.gettype({'a': True, True: False}) == 'dict'
    
    assert g.gettype(float())    == 'float'
    assert g.gettype(0.0)        == 'float'
    assert g.gettype(-0.0)       == 'float'
    assert g.gettype(12.3456789) == 'float'
    assert g.gettype(-9001.001)  == 'float'
    assert g.gettype(12.)        == 'float'
    assert g.gettype(-9001.)     == 'float'
    assert g.gettype(1000 / 11)  == 'float'
    
    assert g.gettype(frozenset()) == 'frozenset'
    
    assert g.gettype(int())     == 'int'
    assert g.gettype(0)         == 'int'
    assert g.gettype(-0)        == 'int'
    assert g.gettype(123)       == 'int'
    assert g.gettype(-123456)   == 'int'
    
    assert g.gettype(list())        == 'list'
    assert g.gettype([])            == 'list'
    assert g.gettype(['j', 26, {}]) == 'list'
    
    assert g.gettype(memoryview(b'')) == 'memoryview'
    
    assert g.gettype(None) == 'NoneType'
    
    assert g.gettype(range(1)) == 'range'
    
    assert g.gettype(set())           == 'set'
    assert g.gettype({1, 2, 'horse'}) == 'set'
    
    assert g.gettype(str())           == 'str'
    assert g.gettype('')              == 'str'
    assert g.gettype('mystring')      == 'str'
    assert g.gettype(f'{69420}blaze') == 'str'
    assert g.gettype(r'\example\n')   == 'str'
    
    assert g.gettype(tuple())         == 'tuple'
    assert g.gettype(())              == 'tuple'
    assert g.gettype((1, 2, 'yeah'))    == 'tuple'
    assert g.gettype((3, f'g', {6, 7})) == 'tuple'
    assert g.gettype((True, 98))      == 'tuple'
    
    print(g.gettype(File))

def test_month2num():
    # print([g.month2num('aug')])
    pass

def test_secmod():
    pass

def test_timestamp():
    # i = 1
    # for a in 0, 1:
    #     for b in 0, 1:
    #         for c in 0, 1:
    #             for d in 0, 1:
    #                 for e in 0, 1:
    #                     for f in 0, 1:
    #                         print(str(i).zfill(2), g.timestamp(a, b, c, d, e, f))
    #                         i += 1
    #         print('\n')
    pass

def test_unpack():
    pass

test_gettype()
test_month2num()
test_secmod()
test_timestamp()
test_unpack()