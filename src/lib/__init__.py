"""
lib
Definitions for the PPSM Dispatcher lib module.
"""

# error codes - range [1:100000], base is 0
error_codes = {'tests': (99901, 100000),
               'locks': (1, 100),
               'ssh': (101, 200),
               'utils': (201, 300),
               'parser': (301, 400),
               'error': (401, 500),
               'core': (501, 600)}
