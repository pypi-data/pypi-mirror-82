# -*- coding: utf-8 -*-
"""
ioflo test package

To run all the unittests:

from ioflo import test
test.run()

"""
import sys
import unittest
import os


from ioflo.aid.consoling import getConsole
console = getConsole()
console.reinit(verbosity=console.Wordage.concise)

start = os.path.dirname(os.path.dirname
                        (os.path.abspath
                            (sys.modules.get(__name__).__file__)))

# need top to be above root for relative imports to not go above top level
top = os.path.dirname(start)

def run(top, start=None, failfast=False):
    """
    Run unittests starting at directory given by start within the package rooted at top
    """
    if not start:
        start = top

    console.terse("\nRunning ioflo tests starting at '{0}' from '{1}', \n".format(start, top))
    loader = unittest.TestLoader()
    suite = loader.discover(start, 'test_*.py', top )
    unittest.TextTestRunner(verbosity=2, failfast=failfast).run(suite)

if __name__ == "__main__":
    run(top, start)
