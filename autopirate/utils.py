__all__ = ('flatmap', 'say', 'norm_path')

import os
import os.path
import syslog
import sys


flatmap = lambda f, l: (i for subl in map(f, l) for i in subl)


def say(message):
  sys.stderr.write("[autopirate] {}\n".format(message))
  syslog.syslog(syslog.LOG_ALERT, message)


norm_path = lambda p: os.path.abspath(os.path.expanduser(p))
