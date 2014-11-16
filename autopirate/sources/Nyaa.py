from collections import deque
from .. import Episode

class NyaaSource(EpisodeSource):
  """
  nyaa.se trusted torrent search
  cats   = 1_37 - English translated only
  filter = 2    - Trusted only
  """
  base_name = "nyaa.se: {}"
  base_url  = "http://www.nyaa.se/?page=rss&cats=1_37&filter=2&{}"

  def __init__(self, name, query):
    self.name  = self.base_name.format(name)
    self.query = query
    self.url   = self.base_url.format(urllib.parse.urlencode({'term': self.query}))

  def fetchEpisodes(self):
    f = feedparser.parse(self.url)
    if f.bozo != 0:
      self.say("Invalid feed or issue with parsing")
      return []
    return flatMap(self.toEpisode, f['entries'])

  def toEpisode(self, i):
    raise NotImplementedError


class HorribleSubsSource(NyaaSource):
  tag      = "[HorribleSubs]"
  titleMap = str.maketrans('._', '  ')

  def __init__(self, shows, path, quality):
    self.shows   = shows
    self.path    = path
    self.quality = quality
    self.query   = "{} {}".format(self.tag, self.quality)
    super().__init__(
      name  = self.tag,
      query = self.query
    )

  def shouldFetch(self, showname):
    for s in self.shows:
      if showname.startswith(s):
        return True
    return False

  def parseTitle(self, title):
    ex = Exception("Unable to parse title: {}".format(title))
    parts = deque(title.translate(self.titleMap).split())
    if parts.popleft() != self.tag:
      raise ex
    parts.pop()  # Strip file extension
    if parts.pop() != self.quality:
      raise ex
    epnum = parts.pop()
    if parts.pop() != '-':
      raise ex
    return (' '.join(parts), epnum)

  def toEpisode(self, i):
    try:
      showname, epnum = self.parseTitle(i['title'])
      if self.shouldFetch(showname):
        return [Episode(
          source   = self.name,
          title    = "",
          showname = showname,
          showid   = showname,
          epid     = epnum,
          link     = i['link'],
          root     = self.path
        )]
    except Exception as e:
      self.say(str(e))
    return []
