import os
from pathlib import Path
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import src.py416.general as g
from src.py416.files import File


@pytest.mark.parametrize('i,o', [
    (0, '0B'),
    (1500, '1.46KiB'),
    (123_456_789, '117.74MiB'),
    (65_487_894_231, '60.99GiB'),
    (875_467_423_467_423, '796.23TiB'),
    (98_700_798_765_465_465, '87.66PiB'),
    (4_317_897_564_234_897_842, '3.75EiB'),
    (12_345_678_901_234_567_890_123, '10.46ZiB'),
    (987_654_321_987_654_321_987_654_321, '816.97YiB'),
    (10**28, '8271.81YiB'),
])
def test_bytesize(i, o):
    assert g.bytesize(i) == o


@pytest.mark.parametrize('i,o', [
    (0, '0B'),
    (1500, '1.50KB'),
    (123_456_789, '123.46MB'),
    (65_487_894_231, '65.49GB'),
    (875_467_423_467_423, '875.47TB'),
    (98_700_798_765_465_465, '98.70PB'),
    (4_317_897_564_234_897_842, '4.32EB'),
    (12_345_678_901_234_567_890_123, '12.35ZB'),
    (987_654_321_987_654_321_987_654_321, '987.65YB'),
    (10**28, '10000.00YB'),
])
def test_bytesize_si(i, o):
    assert g.bytesize(i, si=True) == o


def test_emailsmtp():
    pass


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

    (File(''), 'src.py416.files.File'),
])
def test_gettype(i, o):
    assert g.gettype(i) == o


def test_gettype_Path():
    p = Path()
    if os.name == 'nt':
        assert g.gettype(p) == 'pathlib.WindowsPath'
    elif os.name == 'posix':
        assert g.gettype(p) == 'pathlib.PosixPath'


def test_lineno():
    assert g.lineno() == 127


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


def test_pprint():
    mydict = {
        'a': 1,
        'b': 2_000_000_000,
        'c': 'a happy cat',
        # 'deez nuts': 3.14159_26535_89793_23846_26433,
        34: {1: 'ayy', 2: 'bee'},
        # 'list': [1, 2, 3],
    }
    mylist = [
        'alpha',
        'bravo charlie',
        1234567890,
        2.7,
        [1, 2],
        [4, 5, [6, 7, [8, 9, 10]]],
    ]
    myset = {
        'alpha',
        'bravo charlie',
        1234567890,
        2.7,
        frozenset({1, 2}),
    }
    mytuple = (
        'alpha',
        'bravo charlie',
        1234567890,
        2.7,
        (1, 2),
        (4, 5, (6, 7, (8, 9, 10))),
    )
    mylisttuple = [
        'a',
        ('b',),
        ['c', 'd'],
        ([([('eeeee',)],)],),
    ]


@pytest.mark.parametrize('i,a,o', [
    (3, '', ('03s', 3, 0, 0, 0)),
    (505, ' ', ('08m 25s', 25, 8, 0, 0)),
    (12345, '', ('03h25m45s', 45, 25, 3, 0)),
    (12345678, '--', ('142d--21h--21m--18s', 18, 21, 21, 142)),
    (-46834, ',', ('13h,34s', 34, 0, 13, 0)),
])
def test_secmod(i, a, o):
    assert g.secmod(i, sep=a) == o


@pytest.mark.parametrize('i,o', [
    ('3d16h42m7s', 319327),
    ('1d', 86400),
    ('04h16m02s', 15362),
    ('1s', 1),
    ('2m', 120),
    ('3m4s', 184),
    ('5h', 18_000),
    ('6h7m', 22_020),
    ('8h9s', 28_809),
    ('10h11m12s', 36_672),
    ('13d', 1_123_200),
    ('14d15h', 1_263_600),
    ('16d17m', 1_383_420),
    ('18d19s', 1_555_219),
    ('20d21h22m', 1_804_920),
    ('23d24h25s', 2_073_625),
    ('26d27m28s', 2_248_048),
    ('29d30h31m32s', 2_615_492),
])
def test_secmod_inverse(i, o):
    assert g.secmod_inverse(i) == o


def test_timestamp():
    pass


@pytest.mark.parametrize('i,o', [
    ('', ('',)),
    ([], ()),
    ([1], (1,)),
    ([1, [2]], (1, 2)),
    ([1, (2, [3])], (1, 2, 3)),
    ((), ()),
    ((1,), (1,)),
    ((1, (2,)), (1, 2)),
    ((1, [2, (3,)]), (1, 2, 3)),
    (((((([[[['arf', (65432, 'woof')]], 65]])), 6))), ('arf', 65432, 'woof', 65, 6)),
])
def test_unpack(i, o):
    assert g.unpack(i) == o
