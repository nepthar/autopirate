__all__ = ('EpisodeSource',)

from .utils import say


class EpisodeSource(object):
  "Episode Source Interface"

  name = "Base Source"

  def __str__(self):
    return "<Episode Source {}>".format(self.name)

  def say(self, message):
    say("{}: {}".format(self.name, message))

  def fetchEpisodes(self):
    raise NotImplementedError
