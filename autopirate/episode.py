__all__ = ('Episode',)

import time


class Episode(object):

  def __init__(self, source, title, showname, showid, epid, link, root, created=int(time.time())):
    self.source   = str(source)
    self.title    = title
    self.showname = showname
    self.showid   = showid   # Identify show
    self.epid     = epid     # Identify episode
    self.link     = link     # Something that can be opened with transmission
    self.root     = root     # Where to put this.
    self.uid      = ':'.join((source, showid, epid))
    self.created  = created

  def __eq__(self, other):
    return self.uid == other.uid

  def __lt__(self, other):
    return self.created < other.created

  def __hash__(self):
    return hash(self.uid)

  def __str__(self):
    return '<{}: {} - {}>'.format(self.source, self.showname, self.epid)
