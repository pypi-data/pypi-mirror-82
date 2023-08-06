"""
meta class and base class utility classes and functions

"""
from __future__ import absolute_import, division, print_function

import sys
from collections import Iterable, Sequence
from abc import ABCMeta
import functools
import inspect
import types

# import ioflo modules
from .sixing import *

from .consoling import getConsole
console = getConsole()


def metaclassify(metaclass):
    """
    Class decorator for creating a class with a metaclass.
    This enables the same syntax to work in both python2 and python3
    python3 does not support
        class name(object):
            __metaclass__ mymetaclass
    python2 does not support
        class name(metaclass=mymetaclass):

    Borrowed from six.py add_metaclass decorator

    Usage:
    @metaclassify(Meta)
    class MyClass(object):
        pass
    That code produces a class equivalent to:

    on Python 3
    class MyClass(object, metaclass=Meta):
        pass

    on Python 2
    class MyClass(object):
        __metaclass__ = MyMeta
    """
    def wrapper(cls):
        originals = cls.__dict__.copy()
        originals.pop('__dict__', None)
        originals.pop('__weakref__', None)
        for slots_var in originals.get('__slots__', ()):
            originals.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, originals)
    return wrapper

@metaclassify(ABCMeta)
class NonStringIterable:
    """ Allows isinstance check for iterable that is not a string
    """
    #__metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, C):
        if cls is NonStringIterable:
            if (not issubclass(C, (str, bytes)) and issubclass(C, Iterable)):
                return True
        return NotImplemented

@metaclassify(ABCMeta)
class NonStringSequence:
    """ Allows isinstance check for sequence that is not a string
    """
    #__metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, C):
        if cls is NonStringSequence:
            if (not issubclass(C, (str, bytes)) and issubclass(C, Sequence)):
                return True
        return NotImplemented

def nonStringIterable(obj):
    """
    Returns True if obj is non-string iterable, False otherwise

    Future proof way that is compatible with both Python3 and Python2 to check
    for non string iterables.

    Faster way that is less future proof
    return (hasattr(x, '__iter__') and not isinstance(x, (str, bytes)))
    """
    return (not isinstance(obj, (str, bytes)) and isinstance(obj, Iterable))

def nonStringSequence(obj):
    """
    Returns True if obj is non-string sequence, False otherwise

    Future proof way that is compatible with both Python3 and Python2 to check
    for non string sequences.

    """
    return (not isinstance(obj, (str, bytes)) and isinstance(obj, Sequence) )


def isIterator(obj):
    """
    Returns True if obj is an iterator object, that is,

    has an __iter__ method
    has a __next__ method
    .__iter__ is callable and returns obj

    Otherwise returns False

    """
    if (hasattr(obj, "__iter__") and
        hasattr(obj, "__next__") and
        callable(obj.__iter__) and
        obj.__iter__() is obj
       ):
        return True
    return False



from collections import Generator

def attributize(genfunc):
    """
    Python generators do not support adding attributes.
    Adding support for attributes provides a way to pass information
    from a WSGI App that returns a generator to a WSGI server via the generator

    This decorator takes a Duck Typing approach to decorating
    a generator function or method that returns a new function type instance that
    when called will return a generator like object that supports attributes.
    the new object wrapper or skin acts like a generator but with attributes.

    If genfunc is a generator function then a reference to this wrapper/skin
         is injected as the first positional argument to the orginal
         generator function.
    If genfunc is a generator method, that is, its first parameter is 'self'
        then a reference to this wrapper/skin is injected as the second
        positional argument to the original generator method

    Usage:
    # generator function
    @classing.attributize
    def bar(skin, req=None, rep=None):
        skin._status = 400
        skin._headers = odict(example="Hi")
        yield b""
        yield b""
        yield b"Hello There"
        return b"Goodbye"

    gen = bar()
    msg = next(gen)  # attributes set after first next
    gen._status
    gen._headers

    # generator method
    class R:
        @classing.attributize
        def bar(self, skin, req=None, rep=None):
            self.name = "Peter"
            skin._status = 400
            skin._headers = odict(example="Hi")
            yield b""
            yield b""
            yield b"Hello There " + self.name.encode()
            return b"Goodbye"

    r = R()
    gen = r.bar()
    msg = next(gen)   # attributes set after first next
    gen._status
    gen._headers

    Adding attributes to this injected reference makes them available
    as attributes of the resultant skin

    The new type is AttributiveGenerator

    Parameters:
        genfunc is either
            a generator function that returns a generator object
            a generator method that return a generator object

    Unlike Python functions, Python generators do not support attributes and the
    generator locals dict at .gi_frame.f_locals dissappears once the generator
    is complete so its inconvenient.

    Attributes of generator objects.
    ['.__next__', '__iter__', 'close', 'gi_code', 'gi_frame', 'gi_running',
    'gi_yieldfrom', 'send', 'throw']
    """

    def wrapper(*args, **kwargs):
        """
        When called returns instance of AttributiveGenerator instead of generator.
        """
        def __iter__(self):
            return self

        def send(self):
            raise NotImplementedError

        def throw(self):
            raise NotImplementedError

        tdict = { '__iter__': __iter__, 'send': send, 'throw':  throw,}
        # use type to create dynamic instance of class AttributiveGenerator
        #spec = {'__iter__': lambda self: self, 'send': ,}
        AG = type("AttributiveGenerator", (Generator,), tdict)
        ag = AG()  # create  instance so we can inject it into genfunc

        fargs = inspect.getfullargspec(genfunc).args
        if fargs and fargs[0] == 'self':
            gen = genfunc(args[0], ag, *args[1:], **kwargs)
        else:
            gen = genfunc(ag, *args, **kwargs)  # create generator insert ag ref

        # now add to class references to gen attributes "duckify"
        for attr in ('__next__', 'close', 'send', 'throw',
                     'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom'):
            setattr(AG, attr, getattr(gen, attr))

        functools.update_wrapper(wrapper=ag, wrapped=gen)
        return ag
    return wrapper
