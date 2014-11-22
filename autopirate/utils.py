__all__ = ('flatmap', 'say', 'norm_path', 'enable_stderr')

import os
import os.path
import syslog
import sys

USE_STDERR = False


def enable_stderr():
  global USE_STDERR
  USE_STDERR = True


flatmap = lambda f, l: (i for subl in map(f, l) for i in subl)


def say(message):
  if USE_STDERR:
    sys.stderr.write("[autopirate] {}\n".format(message))
  syslog.syslog(syslog.LOG_NOTICE, message)


norm_path = lambda p: os.path.abspath(os.path.expanduser(p))
