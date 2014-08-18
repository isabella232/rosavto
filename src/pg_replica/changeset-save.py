#!/usr/bin/env python

import re
import os
import sys
import fcntl
import glob
from stat import S_ISREG, ST_CTIME, ST_MODE
import time
import uuid
import base64
import argparse
import datetime
import logging
import requests
import ConfigParser
from crontab import CronTab
import xml.etree.ElementTree as et

from pgdb import *

logger = logging.getLogger('changeset-save')

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    parser = argparse.ArgumentParser()
    parser.add_argument('changeset', help='changeset responce file')
    args = parser.parse_args()
    changeset_file = args.changeset

    config_name = '/etc/pg_replica.conf'
    if not os.path.isfile(config_name):
        logger.critical('Configuration file "%s" not found.' % config_name)
        sys.exit(1)

    cfg = ConfigParser.SafeConfigParser({'log_file': '/var/log/pg_replica.log', 'log_level': 'debug'})

    cfg.read(config_name)
    log_file = cfg.get('logging', 'log_file')
    log_level = cfg.get('logging', 'log_level')
    num_level = getattr(logging, log_level.upper(), None)
    if not isinstance(num_level, int):
        num_level = 10

    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(num_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start logging.')

    if cfg.has_section('path'):
        directory = cfg.get('path', 'changesets')
    else:
        logger.critical('Invalid config file.')
        sys.exit(1)

    logger.debug('Start changeset saving.')

    if not os.path.exists(directory):
        os.makedirs(directory)

    tree = et.parse(changeset_file)
    root = tree.getroot()
    body = root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
    tbl = body.find('tbl').text
    sql = body.find('sql').text

    cfg = ConfigParser.SafeConfigParser()
    cfg.add_section('changeset')
    cfg.set('changeset', 'tbl', tbl)
    cfg.set('changeset', 'sql', sql)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
    with codecs.open(os.path.join(directory, timestamp + '.changeset'), 'wb', 'utf-8') as f:
        cfg.write(f)

    os.remove(changeset_file)

    logger.debug('Stop changesets saving.')
    logger.info('Stop logging.')
    logging.shutdown()