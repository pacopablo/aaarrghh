import os


TEST_PROJECT_INDEX = '.test_company.rst'
TEST_PROJECT_TITLE = 'Corporate Tool'
TEST_PROJECT_DESC = ['Index description.',]
TEST_PROJECT_COMPANY = 'ct'
TEST_PROJECT_CUR_PROJS = ['proj1', 'proj2', 'proj3',]
TEST_PROJECT_CUR_TASKS = ['task1', 'task2', 'task3',]
TEST_PROJECT_FIN_PROJS = ['fin_proj1', 'fin_proj2',]
TEST_PROJECT_FIN_TASKS = ['fin_task1', 'fin_task2',]

TEST_INDEX_ATTRS = {
    'filename' : TEST_PROJECT_INDEX,
    'fin_projs' : TEST_PROJECT_FIN_PROJS,
    'fin_tasks' : TEST_PROJECT_FIN_TASKS,
    'cur_projs' : TEST_PROJECT_CUR_PROJS,
    'cur_tasks' : TEST_PROJECT_CUR_TASKS,
    'company' : TEST_PROJECT_COMPANY,
    'title' : TEST_PROJECT_TITLE,
    'description' : TEST_PROJECT_DESC,
}

TEST_INDEX_MARKUP = """
.. company_ct

**************
Corporate Tool
**************

Index description.

Current Projects:
=================

.. toctree::
   :titlesonly:
   :maxdepth: 1

   ct/proj1
   ct/proj2
   ct/proj3

Current Tasks:
==============

.. toctree::
   :titlesonly:
   :maxdepth: 1

   ct/task1
   ct/task2
   ct/task3

Completed Projects:
===================

.. toctree::
   :titlesonly:
   :maxdepth: 1

   ct/fin_proj1
   ct/fin_proj2

Completed Tasks:
================

.. toctree::
   :titlesonly:
   :maxdepth: 1

   ct/fin_task1
   ct/fin_task2

"""[1:]


def setUp():
    open(TEST_PROJECT_INDEX, 'wb').write(TEST_INDEX_MARKUP)


def tearDown():
    os.unlink(TEST_PROJECT_INDEX)
