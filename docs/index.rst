py416 Introduction
==================

What this package is and hopes to achieve
-----------------------------------------

This is a collection of various functions, mostly for my own personal use in writing scripts for work and other projects. I built this for the following reasons:

- Learn more advanced Python concepts
- Convenience of installing through pip
- Greatly cut down on the amount copy-pasting of code between projects
- Produce something that looks professional and can be used by others
- I abhor Windows' backslashes

The bulk of this package deals with filesystem manipulation as that's what I need it for most. These functions often are a simple wrapper for basic os and shutil functions, but for some they offer extra safety and configurability. For example, by default, os.rename() overwrites a file or folder without warning. Yikes!

This is built in Python 3.8.10 because that is the latest version available on Windows 8, which is required for my work. This is tested on macOS, Ubuntu, and Windows with Python versions 3.8, 3.9, and 3.10. I have no plans to test on older versions, nor to add new features that don't work in 3.8.

.. include:: modules.rst