import os
import sys

import pytest

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')

import src.py416.general as g
from src.py416.files import File

@pytest.mark.parametrize('i,o', [
    (bool(), 'bool'),
    (True, 'bool'),
    (False, 'bool'),

    (bytes(), 'bytes'),
    (b'', 'bytes'),
    (b'hello', 'bytes'),
    (b'\xE2\x82\xAC', 'bytes'),

    (bytearray(), 'bytearray'),

    (complex(), 'complex'),

    (dict(), 'dict'),
    ({}, 'dict'),
    ({1: 2}, 'dict'),
    ({'a': 416, True: False}, 'dict'),

    (float(), 'float'),
    (0.0, 'float'),
    (-0.0, 'float'),
    (12.3456789, 'float'),
    (-9001.001, 'float'),
    (12., 'float'),
    (-9001., 'float'),
    (1000 / 11, 'float'),
    (1000 / 10, 'float'),

    (frozenset(), 'frozenset'),

    (int(), 'int'),
    (0, 'int'),
    (-0, 'int'),
    (123, 'int'),
    (-123456, 'int'),

    (list(), 'list'),
    ([], 'list'),
    (['j', 26, {}], 'list'),

    (memoryview(b''), 'memoryview'),

    (None, 'NoneType'),

    (range(1), 'range'),

    (set(), 'set'),
    ({1, 2, 'horse'}, 'set'),

    (str(), 'str'),
    ('', 'str'),
    ('mystring', 'str'),
    (f'{69420}blaze', 'str'),
    (r'\example\n', 'str'),

    (tuple(), 'tuple'),
    ((), 'tuple'),
    ((45,), 'tuple'),
    ((1, 2, 'yeah'), 'tuple'),
    ((3, f'g', {6, 7}), 'tuple'),
    ((True, 98), 'tuple'),

    (File, 'type'),
])
def test_gettype(i, o):
    assert g.gettype(i) == o

@pytest.mark.parametrize('i,o', [
    ('january', '01'),
    ('February', '02'),
    ('mArCh', '03'),
    ('APRIL', '04'),
    ('may', '05'),
    ('junE', '06'),
    ('july', '07'),
    ('august', '08'),
    ('SEPtember', '09'),
    ('ocTOber', '10'),
    ('november', '11'),
    ('December', '12'),
    ('', ''),
    ('jan', ''),
    ('greq', ''),
    ('March_2022', ''),
    ('AprilApril', ''),
    ('maytheforce', ''),
    ('timeInJune', ''),
    ('where july', ''),
])
def test_month2num(i, o):
    assert g.month2num(i) == o

@pytest.mark.parametrize('i,a,o', [
    (3, '', ('03s', 3, 0, 0, 0)),
    (505, ' ', ('08m 25s', 25, 8, 0, 0)),
    (12345, '', ('03h25m45s', 45, 25, 3, 0)),
    (12345678, '--', ('142d--21h--21m--18s', 18, 21, 21, 142)),
    (-46834, ',', ('13h,34s', 34, 0, 13, 0)),
])
def test_secmod(i, a, o):
    assert g.secmod(i, sep=a) == o

def test_timestamp():
    pass

@pytest.mark.parametrize('i,o', [
    ('', ('')),
    ([], ()),
    ([1], (1,)),
    ([1, [2]], (1, 2)),
    ([1, (2, [3])], (1, 2, 3)),
    ((), ()),
    ((1,), (1,)),
    ((1, (2)), (1, 2)),
    ((1, [2, (3)]), (1, 2, 3)),
    (((((([[[['arf', (65432, 'woof')]], 65]])), 6))), ('arf', 65432, 'woof', 65, 6)),
])
def test_unpack(i, o):
    assert g.unpack(i) == o
