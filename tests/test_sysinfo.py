import os
from pprint import pprint
import sys
import time

import pytest
import pytest_check as check

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.py416.sysinfo as p4s

# pprint(p4s.cpu())
# pprint(p4s.disks(), width=1)
# pprint(p4s.ram(), width=1)
# pprint(p4s.system(), width=100)
# pprint(p4s.users(), width=100)
# pprint(p4s.full(), width=1)

# print(p4s.cpu(json=True))
# print(p4s.disks(json=True))
# print(p4s.ram(json=True))
# print(p4s.system(json=True))
# print(p4s.users(json=True))
# print(p4s.full(json=True))
