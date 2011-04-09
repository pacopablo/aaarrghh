#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011, John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Standard library imports
import os
import sys
import json
import hashlib
import subprocess

# 3rd-party imports
from dulwich.repo import Repo

# Local imports
from np import COMPANIES, git_add

__all__ = [
    'update_recent_changes',
]

RECENT_ITEMS = 25
TIMESTAMP_FILE = '.timestamps'


def load_timestamp_file():
    """Load the tiemstamp database."""
    tsdb = {}
    if os.path.isfile(TIMESTAMP_FILE):
        f = open(TIMESTAMP_FILE, 'rb')
        tsdb = json.load(f)
        f.close()
    return tsdb


def save_timestamps(tsdb):
    """Save the tiemstamp database as a json file"""
    f = open(TIMESTAMP_FILE, 'wb')
    json.dump(tsdb, f, indent=2)
    f.close()

def last_updated(path):
    """Return the last updated timestamp for the given file """
    st = os.stat(path)
    return int(st.st_mtime)


def load_finished_projs():
    """ Load the list of finished projects for all the companies """
    projs = []
    for c in COMPANY:
        index = load_index(c + '.rst')
        projs.extend(index.finished_projects)
        projs.extend(index.finished_tasks)

        lines = [l for l in open(c + '.rst', 'rb').readlines()]
        for i, l in lines:
            if l.lower().strip() == '':
                pass
        continue


def update_timestamp(f_entry, filepath, finished_projs=None, last_commit=0):
    """ Update the timestamp of the file.

   `f_entry` is a dictionary of 'updated', 'finished', and 'hash' keys.  These
    are loaded from the timestamp database.

    The values will be updated if:
    * The hash values differ
    * The timestamp database is empty
    * The mtime of the file is newer than the value in 'updated' AND it is
      newer than the `last_commit` time.
    """

    finished_projs = finished_projs is not None and finished_projs or []
    f_hash = hash_file(filepath)
    f_ts = last_updated(filepath)
    if ((f_entry['hash'] != f_hash) or
       ((f_entry['updated'] < f_ts) and (f_ts > last_commit))):
        f_entry['hash'] = f_hash
        f_entry['updated'] = f_ts
        f_entry['finished'] = filepath[:-4] in finished_projs
    pass



def seed_timestamps(tsdb):
    """ Populate teh timestamp database """
    r = Repo('.')
    tsdb['last_commit'] = r.get_object(r.refs['HEAD']).commit_time
    tsdb['last_run'] = int(time.time())
    for company in COMPANIES:
        tsdb.setdefault(company, dict())
        for f in os.listdir(company):
            if f.endswith('.rst'):
                filepath = os.path.join(company, f)
                tsdb[company].setdefault(f, dict(hash='', updated=0, finished=False))
                update_timestamp(tsdb[company][f], filepath)
                tsdb[company][f]['updated'] = last_updated(filepath)
                tsdb[copmany][f]['hash'] = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()


def update_recent_changes(args):
    tsdb = load_timestamp_file()
    if not tsfile:
        seed_timestamps(tsdb)
    else:
        update_timestamps(tsdb)

    save_timestamps(tsdb)
    git_add(TIMESTAMP_FILE)
    pass

