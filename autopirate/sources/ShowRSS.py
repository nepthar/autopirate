from . import BaseSource
from .. import Episode

class ShowRSS(EpisodeSource):
  name     = "Show RSS"
  url_root = 'http://showrss.info/rss.php?user_id={user_id}&hd=1&proper=0&namespaces=true'

  def __init__(self, user_id, path):
    self.url  = self.url_root.format(user_id=user_id)
    self.path = path

  def toEpisode(self, i):
    try:
      return [Episode(
        source   = self.name,
        title    = i['title'],
        showname = i['showrss_showname'],
        showid   = i['showrss_showid'],
        epid     = i['showrss_episode'],
        link     = i['link'],
        root     = self.path
      )]
    except Exception as e:
      say("Unable to parse item: {}".format(str(e)))
      return []

  def fetchEpisodes(self):
    f = feedparser.parse(self.url)
    if f.bozo != 0:
      self.say('Invalid Feed or issue with parsing.')
      return []
    return flatMap(self.toEpisode, f['items'])
