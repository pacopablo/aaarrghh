.. _design:

Design Document
===============

.. _design_configuration:

Configuration
-------------

Some values, such as *companies* will need to be configured via command line
and/or config file.  `aaarrghh` will look for a config file in the following
places:

* A `.aaarrghrc` in the user's home directory
* An `aaarrgh.ini` in the current directory
* Whatever file is specified on the command line via `--config` / `-c`

The precedence of the files is:

1. `--config` / `-c`
2. `aaarrgh.ini` in the current directory
3. `.aaarrghhrc` in the user's home directory

Values from higher precedence [#]_  levels overwrite those from lower levels.
This means that if a `.aaarrghhrc` is found, as well as an `aaarrghh.ini`,
contents will be merged with the values from `aaarrghh.ini` overriding those
from `.aaarrghhrc`.


Companies
---------

The concept of a *company* is central to the organization of the projects and
tasks.  All projects and tasks must be assigned to a company.  There is no
notion of *global* projects or tasks [#]_.  As the list of companies can not
be hard coded, they must be specified in the :ref:`design_configuration` file

Companies are specified as `key = value` pairs in the `[company]` section.

The key is the internal company identifier.  It should not contain any spaces.
Any spaces in the key will be converted to underscores.  The key is used as
the filename, with `.rst` appended, of the company index.  The company index
holds the TOC for all projects and tasks for the given company.  It is also
referenced from the main index.

The value should contain the company name / title.  It is used on the company
index page as the title.  The value may, and likely will, contain spaces.


Main Index
----------

.. rubric:: Footnotes

.. [#] Where *1* is the highest precedence

.. [#] I am open to revising this stance.  Using *companies* keeps things
       simple and allows for a realitvely nice main TOC.


