import argparse
import transmissionrpc
import os.path
import configparser

from autopirate import *

DEFAULT_CONF='~/.autopirate/conf.ini'

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

parser.add_argument(
  '-d', '--dry-run',
  action = 'store_true',
  help   = 'Display a list of episodes to be download, but do not download them'
)

parser.add_argument(
  '-o', '--output',
  action = 'store_true',
  help   = 'Log to stdout as well as syslog. Default is only syslog'
)

try:
  args = parser.parse_args()

  conf_file = norm_path(args.cf)
  conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
  conf.read(conf_file)

  if args.output:
    enable_stderr()

  tc = transmissionrpc.Client(
    user     = conf.get('transmission', 'user'),
    password = conf.get('transmission', 'pass'),
    port     = int(conf.get('transmission', 'port', fallback='9091'))
  )

  hs_shows = list(filter(
    lambda s: s != '',
    conf.get('HorribleSubs', 'shows').split('\n')
  ))

  source_list = [
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

  say('Checking for new episode')
  state_file = conf.get('ap', 'state_file')
  read_only  = args.dry_run

  with DownloadState(state_file, read_only) as dl:

    for ep in flatmap(lambda s: s.fetchEpisodes(), source_list):
      try:
        if not ep in dl:
          if not args.dry_run:
            os.makedirs(ep.root, exist_ok=True)
            tc.add_torrent(ep.link, download_dir=ep.root)
            dl.add(ep)
          say('Downloading {} --> {}'.format(ep, ep.root))
        else:
          say('Already have {}'.format(ep))
      except transmissionrpc.error.TransmissionError as te:
        say('Error downloading {}: {}'.format(ep, te))

except transmissionrpc.error.TransmissionError as e:
  say('Transmission error: {}'.format(e))
  exit(1)
