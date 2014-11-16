import argparse
import sys
import transmissionrpc
import os.path
import configparser

print("main")
from autopirate import *

parser = argparse.ArgumentParser(
  description = 'Yarr! Piracy be too hard to do manually!'
)
parser.add_argument(
  '-c', '--conf',
  dest    = 'cf',
  action  = 'store',
  help    = 'Config file location.',
  default = '~/.config/autopirate/conf.ini'
)

#try:
args = parser.parse_args()

conf_file = norm_path(args.cf)
conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
conf.read(conf_file)

# tc = transmissionrpc.Client(
#   user     = conf.get('transmission', 'user'),
#   password = conf.get('transmission', 'pass'),
#   port     = int(conf.get('transmission', 'port', fallback='9091'))
# )

dl_state = DownloadState(conf.get('ap', 'state_file'))
dl_root  = conf.get('ap', 'dl')

hs_shows = list(filter(
  lambda s: s != '',
  conf.get('HorribleSubs', 'shows').split('\n')
))

sources = [
  ShowRSS(
    user_id = conf.get('ShowRss', 'user_id'),
    path    = conf.get('ShowRss', 'dl')
  ),
  HorribleSubsSource(
    shows   = hs_shows,
    path    = conf.get('HorribleSubs', 'dl'),
    quality = conf.get('HorribleSubs', 'quality')
  )
]

say('Checking for new episodes')
for e in flatMap(lambda s: s.fetchEpisodes(), sources):
  try:
    if not dl_state.has(e):
      say('Fetching {}'.format(e))
      dl_dir = e.path(dl_root)
      os.makedirs(dl_dir, exist_ok=True)
      #tc.add_torrent(e.link, download_dir=dl_dir)
      dl_state.add(e)
  except transmissionrpc.error.TransmissionError as te:
    say('Transmission: {}'.format(te.message))

dl_state.save()

# except transmissionrpc.error.TransmissionError as e:
#   say('Transmission Client issue: {}. Skipping check'.format(e))
#   sys.exit(1)
