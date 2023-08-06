# -*- coding: utf-8 -*-
"""
Unit Test Template
"""
from __future__ import absolute_import, division, print_function

import sys
import unittest

import os
import datetime

from ioflo.aid.sixing import *
from ioflo.aid.odicting import odict
from ioflo.test import testing
from ioflo.aid.consoling import getConsole
console = getConsole()

from ioflo.aid import timing


def setUpModule():
    console.reinit(verbosity=console.Wordage.concise)

def tearDownModule():
    console.reinit(verbosity=console.Wordage.concise)


class BasicTestCase(unittest.TestCase):
    """
    Example TestCase
    """

    def setUp(self):
        """
        Call super if override so House Framer and Frame are setup correctly
        """
        super(BasicTestCase, self).setUp()
        console.reinit(verbosity=console.Wordage.profuse)

    def tearDown(self):
        """
        Call super if override so House Framer and Frame are torn down correctly
        """
        super(BasicTestCase, self).tearDown()
        console.reinit(verbosity=console.Wordage.concise)

    def testTimestamp(self):
        """
        Test posix timestamp generation
        """
        console.terse("{0}\n".format(self.testTimestamp.__doc__))

        if hasattr(datetime, "timezone"):  # python3.2+
            dt = datetime.datetime.now(datetime.timezone.utc)
            older = (dt - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()
        else:
            dt = datetime.datetime.utcnow()  # not aware
            older = (dt - datetime.datetime(1970, 1, 1)).total_seconds()

        ts = timing.timestamp()
        self.assertNotEqual(ts, 0.0)
        self.assertGreaterEqual(ts, older)

        ts = timing.timestamp(dt=dt)
        self.assertNotEqual(ts, 0.0)
        self.assertEqual(ts, older)


    def testIso8601(self):
        """
        Test iso8601 generation
        """
        console.terse("{0}\n".format(self.testIso8601.__doc__))

        stamp = timing.iso8601()
        self.assertEqual(len(stamp), 26)

        dt = datetime.datetime(2000, 1, 1)
        stamp = timing.iso8601(dt)
        self.assertEqual(stamp, "2000-01-01T00:00:00")

        stamp = timing.iso8601(aware=True)
        if hasattr(datetime, 'timezone'):  # only aware in python3.2+
            self.assertEqual(len(stamp), 32)  # '2017-02-07T23:47:16.498821+00:00'
        else:
            self.assertEqual(len(stamp), 26)  # '2017-08-14T16:19:36.070661'

        if hasattr(datetime, "timezone"):  # python3.2+
            dt = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
            stamp = timing.iso8601(dt, aware=True)
            self.assertEqual(stamp, "2000-01-01T00:00:00+00:00")
        else:
            dt = datetime.datetime(2000, 1, 1)
            stamp = timing.iso8601(dt)
            self.assertEqual(stamp, "2000-01-01T00:00:00")


    def testTuuid(self):
        """
        Test TUUID generation
        """
        console.terse("{0}\n".format(self.testTuuid.__doc__))

        tuid = timing.tuuid()
        self.assertEqual(len(tuid), 24)
        stamp, sep, randomized = tuid.rpartition('_')
        self.assertEqual(sep, '_')
        self.assertEqual(len(stamp), 16)
        self.assertEqual(len(randomized), 7)

        tuid =  timing.tuuid(9)
        self.assertEqual(len(tuid), 24)
        stamp, sep, randomized = tuid.rpartition('_')
        self.assertEqual(sep, '_')
        self.assertEqual(len(stamp), 16)
        self.assertEqual(len(randomized), 7)
        self.assertEqual(stamp[:16], '0000000000895440' )

        tuid =  timing.tuuid(stamp=9, prefix="m")
        self.assertEqual(len(tuid), 26)
        prefix, stamp, randomized = tuid.split('_')
        self.assertEqual(prefix, 'm')
        self.assertEqual(len(stamp), 16)
        self.assertEqual(len(randomized), 7)
        self.assertEqual(stamp[:16], '0000000000895440' )

    def testStamper(self):
        """
        Test Stamper Class
        """
        console.terse("{0}\n".format(self.testStamper.__doc__))

        stamper = timing.Stamper()
        self.assertEqual(stamper.stamp, 0.0)
        stamper.advanceStamp(0.25)
        self.assertEqual(stamper.stamp, 0.25)
        stamper.advance(0.25)
        self.assertEqual(stamper.stamp, 0.5)
        stamper.change(1.5)
        self.assertEqual(stamper.stamp, 1.5)




def runOne(test):
    '''
    Unittest Runner
    '''
    test = BasicTestCase(test)
    suite = unittest.TestSuite([test])
    unittest.TextTestRunner(verbosity=2).run(suite)

def runSome():
    """ Unittest runner """
    tests =  []
    names = [
             'testTimestamp',
             'testIso8601',
             'testTuuid',
             'testStamper',
            ]
    tests.extend(map(BasicTestCase, names))
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runAll():
    """ Unittest runner """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(BasicTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__' and __package__ is None:

    #console.reinit(verbosity=console.Wordage.concise)

    #runAll() #run all unittests

    runSome()#only run some

    #runOne('testBasic')


