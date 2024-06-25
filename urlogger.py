# -*- coding: utf-8 -*-
"""
A class-interface to the Python logging module. If this class is
used, there is no need to 'import logging' in the program that
does the logging.
"""
import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

###
# Other standard distro imports
###
import argparse
import contextlib
import getpass
import logging
from   logging.handlers import RotatingFileHandler
import pathlib

###
# imports and objects that are a part of this project
###
verbose = False

###
# Credits
###
__author__ = "George Flanagin"
__copyright__ = 'Copyright 2023'
__credits__ = "Ivan Sokolovskii ivan3177@github"
__version__ = 0.1
__maintainer__ = ['George Flanagin', 'Alina Enikeeva']
__email__ = ['hpc@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'

def piddly(s:str) -> str:
    """
    A text wrapper for logging the output of multithreaded and
    multiprocessing programs.

    Example: 

        logger=URLogger()
        logger.info(piddly(msg))
    """
    return f": {os.getppid()} <- {os.getpid()} : {s}"


class URLogger: pass

class URLogger:
    __slots__ = {
        'logfile': 'the logfile associated with this object',
        'formatter': 'format string for the logging records.', 
        'level': 'level of the logging object',
        'rotator': 'using the built-in log rotation system',
        'thelogger': 'the logging object this class wraps'
        }

    __values__ = (
        None,
        logging.Formatter('#%(levelname)-8s [%(asctime)s] (%(module)s: %(message)s)'),
        logging.WARNING,
        None,
        None)

    __defaults__ = dict(zip(__slots__.keys(), __values__))

    def __init__(self, **kwargs) -> None:

        # Set the defaults.
        for k, v in URLogger.__defaults__.items():
            setattr(self, k, v)

        # Override the defaults if needed.
        for k, v in kwargs.items(): 
            if k in URLogger.__slots__:
                setattr(self, k, v)
        
        try:
            if self.logfile is None:
                self.logfile=os.path.join(os.getcwd(), "thisprog.log")
            pathlib.Path(self.logfile).touch(mode=0o644, exist_ok=True)

        except Exception as e:
            sys.stderr.write(f"Cannot create or open {self.logfile}. {e}\n")
            raise e from None

        self.rotator = RotatingFileHandler(self.logfile, maxBytes=1<<24, backupCount=2)
            
        self.rotator.setLevel(self.level)
        self.rotator.setFormatter(self.formatter)

        # setting up logger with handlers
        self.thelogger = logging.getLogger('URLogger')
        self.thelogger.setLevel(self.level)
        self.thelogger.addHandler(self.rotator)


    ###
    # These properties provide an interface to the built-in
    # logging functions as if the class member, self.thelogger,
    # were exposed. 
    ###
    @property
    def debug(self) -> object:
        return self.thelogger.debug

    @property
    def info(self) -> object:
        return self.thelogger.info

    @property
    def warning(self) -> object:
        return self.thelogger.warning

    @property
    def error(self) -> object:
        return self.thelogger.error

    @property
    def critical(self) -> object:
        return self.thelogger.critical


    ###
    # Tinker with the object model a little bit.
    ###
    def __str__(self) -> str:
        """ return the name of the logfile. """
        return self.logfile


    def __int__(self) -> int:
        """ return the current level of logging. """
        return self.level


    def __call__(self, level:int) -> URLogger:
        """
        reset the level of logging, and return 'self' so that
        syntax like this is possible:

            mylogger(logging.INFO).info('a new message.')
        """
        self.level = level
        self.rotator.setLevel(self.level)
        self.thelogger.setLevel(self.level)
        return self 


if __name__ == '__main__':
    print("Create a logger.")
    logger = URLogger(level=logging.DEBUG)
    print(f"{int(logger)=}")

    logger.info('This is purely informational') 
    logger.debug('This is a debug message.')
    logger.critical('This is *CRITICAL*')

    with open(str(logger)) as f:
        { print(_) for _ in f.readlines() }
    
