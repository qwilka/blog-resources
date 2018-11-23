# -*- coding: utf-8 -*-
"""
Created on Tue Oct 02 08:25:34 2012

@author: mcens0
"""

import logging
import sys
from os.path import abspath

# Redirect stdout and stderr to a logger in Python Electricmonk.nl
class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''
 
   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())


def setup_logger(logfile="log_messages.txt", lvl=logging.INFO, 
                redir_STOUT=False, redir_STDERR=False,
                frmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    if redir_STOUT:
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl
     
    if redir_STDERR:
        stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl 
    
    logger = logging.getLogger("")
    logger.setLevel(lvl)
    fh = logging.FileHandler(logfile, mode='w')
    formatter = logging.Formatter(frmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if not redir_STOUT and logger.level <= logging.WARN:
        print("Logging application messages to file {}," 
               " if problems check this file.".format( abspath(logfile)) )
    return logger
