__all__ = ('DownloadState',)

import pickle
import time
from datetime import timedelta

from .utils import say, norm_path


class DownloadState:
  """
  DownloadState is a semi-persistent storage of episodes have already been
  downloaded. We make the assumption that re-downloading episodes is not really
  that bad as most torrent clients will recognize this and just mark the files
  as "done". Because of this, failure to load previous state simply issues a
  warning and moves on

  The state file is just a pickled set of episodes. In order to keep the state
  file from growing infinitely, the prune method allows for simple removal of
  old episodes.
  """

  default_prune_age = timedelta(weeks=24)

  def __init__(self, state_file, read_only=False):
    self.state_file = norm_path(state_file)
    self.state      = set()
    self.read_only  = read_only

  def __enter__(self):
    if not self.load():
      say("Warning: Bad or missing state file - Using empty list")
    return self

  def __exit__(self, type, value, traceback):
    if not self.read_only:
      self.save()

  def prune(self, older_than=default_prune_age):
    cutoff = int(time.time() - older_than.total_seconds())
    pruned = set(i for i in self.state if i.created < cutoff)
    self.state -= pruned
    return pruned

  def load(self):
    try:
      with open(self.state_file, 'rb') as f:
        loaded = pickle.load(f)
        if isinstance(loaded, set):
          self.state = loaded
          return True
        else:
          return False
    except (OSError, EOFError, pickle.PickleError):
      return False

  def save(self):
    with open(self.state_file, 'wb') as f:
      pickle.dump(self.state, f)

  def add(self, e):
    return self.state.add(e)

  def __contains__(self, e):
    return e in self.state

  def dump(self):
    return sorted(self.state)
