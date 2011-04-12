.. Aaarrghh documentation master file, created by
   sphinx-quickstart on Mon Apr 11 21:21:39 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Aaarrghh: Project and Task Management
======================================

`aaarrghh` is a tool to help manage projects and tasks via restructrueText and
git.  For details on why restructuredText and git were chosen, read the
:ref:`reasoning`

`aaarrghh` assists in managing the documentation generated when working on
projects and tasks.  It creates new projects and tasks, marks them as
"finished", and handles updating a *Recent Changes* list.

The structure for `aaarrghh` documentation is fairly simple and inflexible
[#]_. Each project or task consists of one `.rst` file.  These are devided
into subdirectories based on the *company* that the project is for.  Each
*company* has an associated `.rst` file that is the table of contents for
projects and tasks for said *company*.  The TOCs of all the companies are
consolidated into a main `index.rst`.  The main `index.rst` aslo contains a
*recent changes* sidebar listing the documents that have changed recently.
There is space in the main `index.rst` to add additional documentation which
pertains to the management process as a whole.  More details can be found in
the :ref:`design`.


Contents:

.. toctree::
   :maxdepth: 2

   reasoning
   design
   api

.. rubric:: Footnotes

.. _[#]: One day I would like `aaarrghh` to be more flexible woth the
   documentation it can handle.  Help very welcome.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

