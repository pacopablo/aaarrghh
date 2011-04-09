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
from StringIO import StringIO


TEMPLATE = "template.rst"

TASK = 't'
PROJECT = 'p'
TYPES = [TASK, PROJECT,]

TITLE_MARKUP_CHAR = '*'
SECTION_MARKUP_CHAR = '='
COMPANY_PREFIX = '.. company_'

PROJECT_SECTIONS = {
    'current projects:': {
        'attr': 'cur_projs',
        'title': 'Current Projects:',
    },
    'current tasks:': {
        'attr': 'cur_tasks',
        'title': 'Current Tasks:',
    },
    'completed projects:': {
        'attr': 'fin_projs',
        'title': 'Completed Projects:',
    },
    'completed tasks:': {
        'attr': 'fin_tasks',
        'title': 'Completed Tasks:',
    },
}

SECTION_ORDER = [
    'current projects:',
    'current tasks:',
    'completed projects:',
    'completed tasks:',
]

TOC_ENTRY_INDENT = '   '
TOC_MARKUP = """
.. toctree::
   :titlesonly:
   :maxdepth: 1
"""

INDEX_ATTRS = {
    'filename' : lambda : None,
    'finished_projs' : lambda : list(),
    'finished_tasks' : lambda : list(),
    'current_projs' : lambda : list(),
    'current_tasks' : lambda : list(),
    'company' : lambda : '',
    'title' : lambda : '',
    'description' : lambda : '',
}


__all__ = ['ProjectIndex',]


class ProjectIndex(object):
    """ Class that represents a project index."""

    def __init__(self, indexfile=None):
        """ Load the index file """
        for attr, default in INDEX_ATTRS.items():
            setattr(self, attr, default())
        self.filename = indexfile
        self.load_index(filename=self.filename)
        pass


    def reset(self):
        for attr, default in INDEX_ATTRS.items():
            setattr(self, attr, default())
        pass


    def load_index(self, filename=None, fp=None):
        """ Load the index

        :param filename: File from which the index is loaded.  If `None`, the
                         file name specified in `self.filename` is used.  If
                         `self.filename` is `None`, an empty index is created.

        :type filename: str
        :param fp: File like object from which to read the data.
        """
        close = False
        filename = filename or self.filename
        self.filename = filename
        if not (fp or filename):
            self.reset()
            return

        if not fp and filename:
            fp = open(filename, 'rb')
            close = True

        # Pull out the copmany
        self.company = filename and filename[:-4] or ''

        lines = fp.readlines()
        self.company = self._get_company(lines)
        self.title = self._get_title(lines)
        self.description = self._get_description(lines)
        for section, data in PROJECT_SECTIONS.items():
            setattr(self, data['attr'], self._get_section(section, lines))
            continue

        if close:
            fp.close()
        pass


    def dump_index(self, filename=None, fp=None):
        """ Dump the index.

        :param filename: Name of file into which the index will be written.
        :type filename: str
        :param fp:  If sepcified, the index will be dumped to the file-like
                    object specified.  Otherwise, it will be dumped to the
                    file from which it was loaded.
        """
        close = False
        filename = filename or self.filename
        if not fp:
            fp = open(filename, 'wb')
            closefp = True

        outlines = []
        outlines.append(COMPANY_PREFIX + self.company + '\n')
        outlines.append(TITLE_MARKUP_CHAR * len(self.title))
        outlines.append(self.title)
        outlines.append(TITLE_MARKUP_CHAR * len(self.title) + '\n')
        outlines.append('\n'.join(self.description) + '\n')
        for section in SECTION_ORDER:
            title = PROJECT_SECTIONS[section]['title']
            outlines.append(title)
            outlines.append(SECTION_MARKUP_CHAR * len(title))
            outlines.append(TOC_MARKUP)
            for proj in getattr(self, PROJECT_SECTIONS[section]['attr'], []):
                outlines.append(TOC_ENTRY_INDENT + self.company + '/' + proj)
                continue
            outlines.append('')
            continue
        outlines.append('')
        fp.write('\n'.join(outlines))

        if close:
            fp.close()
        pass


    def dumps_index(self):
        """ Return a string representation of the index """
        s = StringIO()
        self.dump_index(fp=s)
        return s.getvalue()


    # Internal Parsing methods
    def _get_title_boundaries(self, l, index, markup_char, start_idx=-1, end_idx=-1):
        num_markup_chars = l.strip().count(markup_char)
        if num_markup_chars and (num_markup_chars == len(l.strip())):
            if start_idx < 0:
                start_idx = index
            elif end_idx < 0:
                end_idx = index;
        return start_idx, end_idx


    def _get_title(self, lines):
        """ Return the Index title. """
        start_idx = end_idx = -1
        title = ''
        for i, l in enumerate(lines):
            start_idx, end_idx = self._get_title_boundaries(l, i,
                                        TITLE_MARKUP_CHAR, start_idx, end_idx)
            continue
        if ((start_idx + 1) == (end_idx - 1)) and ((start_idx + 1) < len(lines)):
            title = lines[start_idx + 1]
        return title.strip()

    def _get_company(self, lines):
        """ Return the company name """
        company_line = [l.strip() for l in lines if l.startswith(COMPANY_PREFIX)]
        if company_line:
            company = company_line[0][len(COMPANY_PREFIX):].strip()
        else:
            company = self.filename and self.filename[:-4] or ''
        return company


    def _get_description(self, lines):
        start_idx = end_idx = project_start_idx = -1
        for i, l in enumerate(lines):
            start_idx, end_idx = self._get_title_boundaries(l, i,
                                        TITLE_MARKUP_CHAR, start_idx, end_idx)
            if l.strip().lower() in PROJECT_SECTIONS.keys():
                project_start_idx = i
            if (start_idx >= 0) and (end_idx >= 0) and (project_start_idx >= 0):
                break
            continue
        description = []
        if end_idx < project_start_idx:
            description = [l.strip() for l in lines[end_idx + 1:project_start_idx] if l.strip()]
        return description


    def _get_section(self, section, lines):
        start_idx = end_idx = -1
        sections = PROJECT_SECTIONS.keys()
        sections.remove(section)
        for i, l in enumerate(lines):
            if l.strip().lower() == section:
                start_idx = i
            elif (start_idx >= 0)  and (l.strip().lower() in sections):
                end_idx = i
                break
            continue

        section_data = lines[start_idx:end_idx]
        breaks = []
        for i, l in enumerate(section_data):
            if not l.strip():
                breaks.append(i)
            continue
        if len(breaks) == 2:
            breaks.append(len(section_data))
        elif len(breaks) < 3:
            return []

        proj_start = breaks[1] + 1
        proj_end = breaks[2]
        projects = []
        for l in section_data[proj_start:proj_end]:
            projects.append(l.strip().split('/')[-1])
            continue

        return projects


