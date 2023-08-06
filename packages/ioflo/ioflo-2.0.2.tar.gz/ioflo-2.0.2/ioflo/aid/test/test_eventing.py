# -*- coding: utf-8 -*-
"""
Unit Test Template
"""
from __future__ import absolute_import, division, print_function

import sys
import datetime
import unittest

import os
import time

from ioflo.aid.sixing import *
from ioflo.aid.odicting import odict
from ioflo.test import testing
from ioflo.aid.consoling import getConsole
from ioflo.aid.timing import iso8601, tuuid

console = getConsole()

from ioflo.aid import eventing


def setUpModule():
    console.reinit(verbosity=console.Wordage.concise)

def tearDownModule():
    pass


class BasicTestCase(unittest.TestCase):
    """
    Example TestCase
    """

    def setUp(self):
        """
        Call super if override so House Framer and Frame are setup correctly
        """
        super(BasicTestCase, self).setUp()

    def tearDown(self):
        """
        Call super if override so House Framer and Frame are torn down correctly
        """
        super(BasicTestCase, self).tearDown()

    def testTagify(self):
        """
        Test tagify function
        """
        console.terse("{0}\n".format(self.testTagify.__doc__))
        console.reinit(verbosity=console.Wordage.profuse)

        tag = eventing.tagify()
        self.assertEqual(tag, u'')

        tag = eventing.tagify(head='exchange')
        self.assertEqual(tag, 'exchange')

        tag = eventing.tagify(head=['exchange', 'trade'])
        self.assertEqual(tag, 'exchange.trade')

        tag = eventing.tagify(head='exchange', tail='completed')
        self.assertEqual(tag, 'exchange.completed')

        tag = eventing.tagify(head='exchange', tail=['process', 'started'])
        self.assertEqual(tag, 'exchange.process.started')

        tag = eventing.tagify(head=['exchange', 'trade'], tail=['process', 'started'])
        self.assertEqual(tag, 'exchange.trade.process.started')

        tag = eventing.tagify(head=['exchange', 'trade'], tail='completed')
        self.assertEqual(tag, 'exchange.trade.completed')

        tag = eventing.tagify(head='exchange', tail=['process', 'started'], sep='/')
        self.assertEqual(tag, 'exchange/process/started')

        tag = eventing.tagify(tail=['process', 'started'])
        self.assertEqual(tag, 'process.started')

        console.reinit(verbosity=console.Wordage.concise)

    def testEventify(self):
        """
        Test eventify function
        """
        console.terse("{0}\n".format(self.testEventify.__doc__))
        console.reinit(verbosity=console.Wordage.profuse)

        dt = datetime.datetime.utcnow()
        stamp = dt.isoformat()
        time.sleep(0.01)

        event = eventing.eventify('hello')
        self.assertEqual(event['tag'], 'hello')
        self.assertEqual(event['data'], {})
        #"YYYY-MM-DDTHH:MM:SS.mmmmmm"
        tdt = datetime.datetime.strptime(event['stamp'], "%Y-%m-%dT%H:%M:%S.%f")
        self.assertGreater(tdt, dt)

        event = eventing.eventify(tag=eventing.tagify(head='exchange', tail='started'),
                                stamp=stamp)
        self.assertEqual(event['tag'], 'exchange.started' )
        self.assertEqual(event['stamp'], stamp )

        event = eventing.eventify(tag=eventing.tagify(tail='started', head='exchange'),
                                stamp=stamp,
                                data = odict(name='John'))
        self.assertEqual(event['tag'], 'exchange.started')
        self.assertEqual(event['stamp'], stamp)
        self.assertEqual(event['data'], {'name':  'John',})

        stamp = '2015-08-10T19:26:47.194736'
        event = eventing.eventify(tag='process.started', stamp=stamp, data={'name': 'Jill',})
        self.assertEqual(event, {'tag': 'process.started',
                                 'stamp': '2015-08-10T19:26:47.194736',
                                 'data': {'name': 'Jill',},})

        event = eventing.eventify(tag="with uid", stamp=stamp, uid="abcde")
        self.assertEqual(event, {'data': {},
                                'stamp': '2015-08-10T19:26:47.194736',
                                'tag': 'with uid',
                                'uid': 'abcde'})

        console.reinit(verbosity=console.Wordage.concise)

    def testEventize(self):
        """
        Test eventize function
        """
        console.terse("{0}\n".format(self.testEventize.__doc__))
        console.reinit(verbosity=console.Wordage.profuse)


        stamp = iso8601()  # "YYYY-MM-DDTHH:MM:SS.mmmmmm"
        tuid = tuuid()  # "0000014ddf1f2f9c_5e36738"
        time.sleep(0.1)

        event = eventing.eventize('hello')
        self.assertEqual(event['tag'], 'hello')
        self.assertFalse('data' in event)
        self.assertFalse('stamp' in event)
        self.assertFalse('uid' in event)
        self.assertFalse('route' in event)

        event = eventing.eventize(tag=eventing.tagify(head='exchange', tail='started'),
                                  stamp=True,
                                  uid=True,
                                  data=True,
                                  route=odict([("src", (None, None, None)),
                                             ("dst", (None, None, None))]))


        self.assertEqual(event['tag'], 'exchange.started')
        self.assertTrue('data' in event)
        self.assertIsInstance(event["data"], odict)
        self.assertEqual(event['data'], odict([]))
        self.assertTrue('stamp' in event)
        self.assertIsInstance(event["stamp"], str)
        self.assertGreater(event['stamp'], stamp)
        self.assertTrue('uid' in event)
        self.assertIsInstance(event["uid"], str)
        self.assertGreater(event['uid'], tuid)
        self.assertTrue('route' in event)
        self.assertEqual(event['route'] ,odict([("src", (None, None, None)),
                                         ("dst", (None, None, None))]))

        event = eventing.eventize(tag=eventing.tagify(head='exchange', tail='started'),
                                  stamp=stamp,
                                  uid=tuid,
                                  data=odict(name="John"),
                                  route=odict([("src", (None, None, None)),
                                             ("dst", (None, None, None))]))


        self.assertEqual(event['tag'], 'exchange.started')
        self.assertEqual(event['data'], odict(name="John"))
        self.assertEqual(event['stamp'], stamp)
        self.assertEqual(event['uid'], tuid)
        self.assertEqual(event['route'] ,odict([("src", (None, None, None)),
                                         ("dst", (None, None, None))]))



        console.reinit(verbosity=console.Wordage.concise)


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
             'testTagify',
             'testEventify',
             'testEventize',
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


