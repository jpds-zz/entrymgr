#!/usr/bin/python
#
#   entrymgr.py: Main entrymgr code base.
#
#   Copyright (C) 2013, Jonathan Davies <jpdavs@gmail.com>
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
#

__author__ = "Jonathan Davies"
__copyright__ = "Copyright 2013, Jonathan Davies"
__license__ = "BSD"

import argparse
import os
import sys

from datetime import datetime

def formulate_directory_structure(date):
    # Create a directory structure based on the date.
    structure = date.strftime('%Y/%m/%d')
    return structure

def ensure_directory_exists(dir_structure):
    # Make sure that the directory structure for our entry exists.
    if not os.path.isdir(dir_structure):
        os.makedirs(dir_structure)

    return True

def check_entry_exists(target_file):
    # Check if an entry already exists or not.
    return os.path.isfile(target_file)

def generate_datestamp(entry_date):
    # Create a valid datetime object based on the inputted string.
    datestamp = datetime.strptime(entry_date, "%Y/%m/%d")

    return datestamp

def split_datestamp_string(date_string):
    # Helper function that's given a date in YYYY/MM/DD, and returns YYYY, MM,
    # DD.

    year, month, day = date_string.split("/")

    return (year, month, day)

def expunge_directory_if_empty(directory_structure):
    # Remove a directory if it has no entries.

    year, month, day = split_datestamp_string(directory_structure)

    for i in day, month, year:
        position_of_i = directory_structure.index(i) + len(i)
        target_directory = directory_structure[0:position_of_i]
        if len(os.listdir(target_directory)) is 0:
            os.rmdir(target_directory)

def create_entry(entry_name,
                 entry_date):
    #
    #   Create a journal entry.
    #
    # Place it in a directory such as YYYY/MM/DD/entry-name.md

    directory_structure = formulate_directory_structure(entry_date)

    ensure_directory_exists(directory_structure)

    target_file = "%s/%s.md" % (directory_structure,
                                entry_name.replace(" ", "-").lower())

    if check_entry_exists(target_file):
        raise argparse.ArgumentTypeError(
                "Entry with filename '%s' exists." % target_file)

    entry_file = open(target_file, 'w')

    entry_file.write("%s\n" % entry_name)

    # Put in a heading into our file in Markdown.
    for x in entry_name:
        entry_file.write("=")

    # Write new line to file.
    entry_file.write("\n")

def delete_entry(entry_name,
                 entry_date):
    # Delete an entry.
    directory_structure = formulate_directory_structure(entry_date)
    target_file = "%s/%s.md" % (directory_structure,
                                entry_name.replace(" ", "-").lower())

    if not check_entry_exists(target_file):
        raise argparse.ArgumentTypeError(
                "Entry with filename '%s' does not exist." % target_file)

    os.unlink(target_file)
    expunge_directory_if_empty(directory_structure)

def main():
    # First of all: parse our arguments and verify them.
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Manage journal entries.")
    parser.add_argument(
            'action',
            help="Action to perform on entry, one of: create, remove."
            )
    parser.add_argument(
            '--name',
            help="Name of entry to perform action on.",
            )
    parser.add_argument(
            '--date',
            help="Date of entry to perform action on (Format: YYYY/MM/DD).",
            default=datetime.now(),
            )

    args = parser.parse_args()

    if args.action not in ("create", "remove"):
        raise argparse.ArgumentTypeError("Invalid action.")

    if args.name is None:
        raise argparse.ArgumentTypeError("No entry name specified.")

    date = args.date

    if isinstance(args.date, str):
        date = generate_datestamp(args.date)

    if args.action in "create":
        create_entry(args.name, date)
    elif args.action in "remove":
        delete_entry(args.name, date)

    print("%sd entry '%s' for %s." % (args.action.capitalize(),
                                      args.name, date.strftime('%Y/%m/%d')))
