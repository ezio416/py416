import os
import sys

import pytest
import pytest_check as check

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.py416.json as p4j


def test_pretty(tmp_path):
    pass
#     print(p4j.pretty(tmp_path))


# if __name__ == '__main__':
#     test_pretty(r'C:\Users\Ezio\Code\trackmania-json-tracking')
