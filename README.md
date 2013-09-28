entrymgr
========

entrymgr is a command-line based diary-entry management tool which can use a
DVCS as a backend for history tracking.

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

If the entry was the sole entry for that date, the date's directory will be
automagically removed.

Test suite
----------

To run the test suite that comes with entrymgr, run this command in this
directory:

    $ python -m unittest discover tests
