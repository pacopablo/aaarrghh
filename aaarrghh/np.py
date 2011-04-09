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
import argparse
import subprocess
from pprint import pprint

VERSION = '1.0'

TEMPLATE = "template.rst"
TOC_ENTRY_INDENT = '   '

ADD = 'a'
FINISH = 'f'
LIST = 'l'
UPDATE_RECENT = 'u'
ACTIONS = [ADD, FINISH, LIST, UPDATE_RECENT,]
TASK = 't'
PROJECT = 'p'
TYPES = [TASK, PROJECT,]

COMPANIES = ['pc', 'eg', 'ag',]

INDEXES = {
    'pc': 'pc.rst',
    'eg': 'eg.rst',
    'ag': 'ag.rst',
}

SECTIONS = {
    'current projects:': ADD + PROJECT,
    'current tasks:': ADD + TASK,
    'completed projects:': FINISH + PROJECT,
    'completed tasks:': FINISH + TASK,
}

RECENT_ITEMS = 25
TIMESTAMP_FILE = '.timestamps'


def git_add(filename):
    """ Add a file to the git repos """
    subprocess.call(['git', 'add', filename])


def get_value(opts, key, prompt_txt="Enter value: ", prompt=True):
    """ Return the value of the given command line option

    If the option was not specified on the command line, prompt for it.

    :param opts: argparse.Namespace instance holding the command line parameters
    :param key: the name of the argparse option for which a value should be found
    :type key: str
    :param prompt_txt: Text to show when prompting for a value.
    :type prompt_txt: str
    :param prompt: if False, the user will not be prompted for the value if it is
                   not specified otherwise.
    :type prompt: boolean
    :rtype str:

    """

    value = getattr(opts, key, None) or ''
    if prompt:
        value = value or raw_input(prompt_txt)
    return value


def get_project_document(args):
    """ Return the project document.

    If not specified on the command line, the user is prompted for the project
    document.  Additionally, if the document name contains spaces, the user
    will be re-prompted.
    """

    doc = get_value(args, 'doc', 'Enter project document (w/o .rst): ')
    while doc.find(' ') >= 0:
        print('Please do not include spaces in the project document name.')
        doc = get_value(args, 'doc', 'Enter project document (w/o .rst): ')
        continue
    return doc


def get_project_company(args):
    """ Return the project company.

    If not specified on the command line, the user is promted for the project
    company.  Additionally, if the company is not in COMPANIES, the user is
    re-prompted.
    """

    # TODO: generate list of valid companies in prompts based on COMPANIES.
    company = get_value(args, 'company', 'Enter company [pc|eg|ag]: ').lower()
    while company not in COMPANIES:
        print("A company must be selected.  Please choose between pc, eg, and ag.")
        company = get_value(args, 'company', 'Enter company [pc|eg|ag]: ').lower()
        continue
    return company


def write_skeleton_file(name, doc, company, noedit=False):
    """ Write a new project document based on the template """

    if not os.path.exists(company):
        os.mkdir(company)
    destpath = os.path.join(company, doc + r'.rst')
    dest = open(destpath, 'wb')
    for l in open(TEMPLATE, 'rb').readlines():
        line = l.replace('<project_name>', name)
        line = line.replace('<project_document>', doc)
        dest.write(line)
        continue
    dest.close()
    if not noedit:
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, destpath])
    git_add(destpath)
    pass


def update_index_add_doc(doc, company, doc_type):
    """ Add a project document to the appropriate index file """
    indexfile = INDEXES[company]
    outlines = []
    buffer = []
    current_section = ''
    done = False
    for l in open(indexfile, 'rb').readlines():
        if l.lower().strip() in SECTIONS.keys():
            if current_section == (ADD + doc_type):
                outlines.extend(buffer[:-1])
                outlines.append(TOC_ENTRY_INDENT + company + '/' + doc + '\n')
                outlines.append('\n')
                done = True
            else:
                outlines.extend(buffer)
            buffer = [l]
            current_section = SECTIONS[l.lower().strip()]
        else:
            buffer.append(l)
        continue
    if not done and (current_section == (ADD + doc_type)):
        outlines.extend(buffer[:-1])
        outlines.append(TOC_ENTRY_INDENT + company + '/' + doc + '\n')
        outlines.append('\n')
        done = True
    else:
        outlines.extend(buffer)
    open(indexfile, 'wb').writelines(outlines)
    git_add(indexfile)
    pass


def update_index_finish_doc(doc, company, doc_type):
    """ Move document to "completed" section """
    indexfile = INDEXES[company]
    lines = open(indexfile, 'rb').readlines()
    section_indexes = {}
    doc_index = -1
    current_section = ''
    for i, l in enumerate(lines):
        if l.lower().strip() == (company + '/' + doc):
            doc_index = i
        section = l.lower().strip()
        if section in SECTIONS.keys():
            section_key = SECTIONS[section]
            if current_section != section_key:
                if current_section:
                    section_indexes[current_section]['end'] = i - 1
                section_indexes.setdefault(section_key, dict(start=i))
                current_section = section_key
        continue
    if current_section:
        section_indexes[current_section]['end'] = i
    l = lines.pop(doc_index)
    end_index = section_indexes[FINISH + doc_type]['end']
    if end_index >= doc_index:
        end_index -= 1
    lines.insert(end_index, l)
    open(indexfile, 'wb').writelines(lines)
    git_add(indexfile)
    pass


def list_projects(doc, company, doc_type):
    """ Lists the projects.

    Company, doc type, and doc may be specified to limit list
    """
    print("TODO")


def get_yesno(message, default=False):
    """ Prints the given message and prompts for [y/n]

    A default may be specified.  If True, then a `y` response will be given
    if not input is received.  If False, then `n`.  If `None` is specified,
    a response will be required.
    """
    if default:
        prompt = ' [Y/n]: '
    elif default is False:
        prompt = ' [y/N]: '
    elif default is None:
        prompt = ' [y/n]: '
    val = raw_input(message + prompt)
    while (val.lower() not in ['y', 'n']) and (default is None):
        val = raw_input(message + prompt)
        continue

    if val:
        ret = val == 'y'
    else:
        ret = default
    return ret


def main(args):
    if args.action == ADD:
        # Get the values we need to add a document
        name = get_value(args, 'name', 'Enter project name: ')
        doc = get_project_document(args)
        company = get_project_company(args)

        # Check if file exists and get confirmation if so.
        replace = True
        filename = os.path.join(company, doc + '.rst')
        if os.path.exists(filename):
            replace = get_yesno("The document {} already exists.  "
                                "Do you want to replace it? [y/N]: ".format(
                                filename))
        if replace:
            # Write out the new project file
            write_skeleton_file(name, doc, company, args.noedit)

            # Udpate the appropriate index
            update_index_add_doc(doc, company, args.type)
    elif args.action == FINISH:
        # Get the values we need to finish a document
        doc = get_project_document(args)
        company = get_project_company(args)

        # Update appropriate index
        update_index_finish_doc(doc, company, args.type)
    elif args.action == LIST:
        list_projects(args.doc, args.company, args.type)
    elif args.action == UPDATE_RECENT:
        update_recent_changes(args)
    else:
        print("Please specify whether to add or finish the document")


def doArgs(argv):
    """ Configure ArgumentParser and parse command line arguments """

    global VERSION
    description = "Add and finish projects and tasks"
    usage = "%(prog)s [options]"

    parser = argparse.ArgumentParser(prog='np.py', description=description,
                                     usage=usage)
    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument('--name', default=None,
                        help="Project name.")
    parser.add_argument('--doc', default=None,
                        help="Project file name, with out .rst extension")
    parser.add_argument('--noedit', default=False, action='store_true',
                        help="Do not launch the editor after creating a file.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--task', '-t', action='store_const', const=TASK,
                       dest='type', help="The project type is \"task\"")
    group.add_argument('--project', '-p', action='store_const', const=PROJECT,
                        dest='type', help="The project type is \"project\"")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', action='store_const',
                        const=ADD, dest='action', help="Add a new project.")
    group.add_argument('--finish', action='store_const', const=FINISH,
                        dest='action', help="Finish a project")
    group.add_argument('--list', action='store_const', const=LIST,
                        dest='action', help="List projects")
    parser.add_argument('--update-recent-changes', const=UPDATE_RECENT,
                        action='store_const', dest='action',
                        help='Update the "Recent Changes" section')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pc', action='store_const', const='pc', dest='company',
                        help="Operate on pc projects")
    group.add_argument('--eg', action='store_const', const='eg', dest='company',
                        help="Operate on eg projects")
    group.add_argument('--ag', action='store_const', const='ag', dest='company',
                        help="Operate on ag projects")

    opts = parser.parse_args(argv)

    opts.index_section_target = opts.action + opts.type
    if not getattr(opts, 'type', None):
        opts.type = None
    if not getattr(opts, 'company', None):
        opts.company = None

    #TODO: Need logic in here validating opts.config.  If option is --pillage,
    #      need to make sure we can write the file.  Otherwise, need to be
    #      verify read of file.
    return opts


if __name__ == '__main__':
    opts = doArgs(sys.argv[1:])
    sys.exit(main(opts))


