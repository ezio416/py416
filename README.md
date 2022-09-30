# py416

[![tests](https://github.com/ezio416/py416/actions/workflows/tests.yml/badge.svg)](https://github.com/ezio416/py416/actions)
[![docs](https://readthedocs.org/projects/py416/badge/?version=latest)](https://py416.readthedocs.io/en/latest/)
[![PyPI](https://badge.fury.io/py/py416.svg)](https://pypi.org/project/py416/)
[![license](https://img.shields.io/badge/license-LGPL%20v2.1-red.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)

What this package is and hopes to achieve
-----------------------------------------

This is a collection of various functions, mostly for my own use in writing scripts for work and personal projects. I built this for the following reasons:

- Learn more advanced Python concepts
- Convenience of installing through pip
- Greatly cut down on the amount copy-pasting of code between projects
- Produce something that looks professional and can be used by others
- I abhor Windows' backslashes

The bulk of this package deals with filesystem manipulation as that's what I need it for most. A lot of these functions are just wrappers for basic os and shutil functions with some extra safety, configurability, and normalization.

This is built in Python 3.8 because it's the latest version available on Windows 8, which is required for my work. This is automatically tested on macOS, Ubuntu, and Windows with Python versions 3.8, 3.9, and 3.10. I have no plans to test on older versions, nor to add new features that don't work in 3.8, such as dict union operators (3.9) or match (3.10).