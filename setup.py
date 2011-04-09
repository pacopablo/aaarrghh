#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from setuptools import setup

setup(
    name = 'aaarrghh',
    version = '0.1',
    author = 'John Hampton',
    author_email = 'pacopablo@pacopablo.com',
    url = 'http://aaarrghh.rtfd.org/',
    description = 'Project / Task documentation system using Sphinx and Git',
    license = 'BSD',
    zip_safe = False,
    packages = ['aaarrghh'],
    scripts = ['scripts/aaarrghh'],
    install_requires = ['Sphinx', 'dulwich',],
    setup_requires = ['nose',],
)
