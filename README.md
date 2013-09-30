entrymgr
========

entrymgr is a command-line-based journal entry management tool which can make
use of a DVCS as a backend for history tracking and file replication.

It can be used, for example, to maintain a text-based diary, or a journal of
server changes.

Managing entries
----------------

An entry for today can be created running:

    $ entrymgr create --name "Starting off"

This will create a directory structure based on YYYY/MM/DD such as:

    2013
    └── 09
        └── 28
            └── starting-off.md

Optionally, a date can be specified using the --date option:

    $ entrymgr create --name "Trip to Mars" --date "2038/08/09"

Similarly, entries can be removed with the following:

    $ entrymgr remove --name "Starting off"

Upon the running of the remove action, entrymgr will go through each of the
entry's parent directories and remove them if they have no elements within
them. In the tree example above, 28 would be removed, then 09, then 2013 as they
have no children.

Test suite
----------

To run the test suite that comes with entrymgr, run this command in this
directory:

    $ python -m unittest discover tests

The test suite must also be ran before every commit by using the included
pre-commit.sh script:

    $ ln -s ../../pre-commit.sh .git/hooks/pre-commit
