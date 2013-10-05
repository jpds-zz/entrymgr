#!/usr/bin/python
#
#   This file contains the test suite for entrymgr.
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

import argparse
import datetime
import os
import shutil
import sys
import unittest

sys.path.append("..")

os.environ['LANGUAGE'] = 'en'

import entrymgr

class EntryMgrFakeJournalTestCase(unittest.TestCase):
    def setUp(self):
        entrymgr.ensure_directory_exists("tests/fakejournal")
        os.chdir("tests/fakejournal")

    def tearDown(self):
        # Remove the above directory.
        os.chdir("../..")
        shutil.rmtree("tests/fakejournal")

class EnsureDirectoryExists(unittest.TestCase):
    # Test our entrymgr.ensure_directory_exists() function works.
    _date = "2013/09/23"
    _target_test_directory = "tests/fakejournal/"

    def runTest(self):
        # Create the directory structure based on the fake date above.
        entrymgr.ensure_directory_exists(
            self._target_test_directory + self._date)

        self.assertTrue(os.path.isdir(
            self._target_test_directory + self._date))

    def tearDown(self):
        # Remove the above directory.
        shutil.rmtree(self._target_test_directory)

class FormulateDateStructureTestCase(unittest.TestCase):
    # Make sure that we create proper strings.
    def runTest(self):
        fake_date = datetime.datetime(2004, 2, 12)
        function_result = entrymgr.formulate_directory_structure(fake_date)
        self.assertEqual(function_result, "2004/02/12")

class CheckLicenseTestCase(unittest.TestCase):
    # Simple dummy test to ensure that even unittest is working.
    def runTest(self):
        self.assertEqual(entrymgr.__license__, "BSD")

class GenerateDatestampTestCase(unittest.TestCase):
    # Ensure that we can generate valid datestamps for entry directories.
    def test_datetime_function_return_valid(self):
        control = datetime.datetime(2018, 12, 25)
        date = entrymgr.generate_datestamp("2018/12/25")
        self.assertEqual(date, control)

    def test_invalid_date_input_caught(self):
        with self.assertRaises(ValueError) as test_exception:
            date = entrymgr.generate_datestamp("2008/13/20")

class CheckEntryExistsTestCase(EntryMgrFakeJournalTestCase):
    _entry_title = "Checking Entry Exists"
    _entry_date = entrymgr.generate_datestamp("2000/01/01")

    def runTest(self):
        target_filepath = "2000/01/01/checking-entry-exists.md"
        self.assertFalse(entrymgr.check_entry_exists(
            target_filepath))
        entrymgr.create_entry(self._entry_title, self._entry_date)
        self.assertTrue(entrymgr.check_entry_exists(
            target_filepath))

class EntryLifeCycleTestCase(EntryMgrFakeJournalTestCase):
    # Ensure that we can create an entry.
    _entry_title = "Testing Lifecycle"
    _entry_date = entrymgr.generate_datestamp("2013/05/18")
    _target_result = "Testing Lifecycle\n=================\n"

    def runTest(self):
        target_filepath = "2013/05/18/testing-lifecycle.md"

        # Ensure that we can create an entry.
        entrymgr.create_entry(self._entry_title, self._entry_date)

        # Make sure contents are sane.
        entry_file = open(target_filepath, 'r')
        entry_text = entry_file.read()
        entry_file.close()

        self.assertEqual(entry_text, self._target_result)
        self.assertTrue(os.path.isfile(target_filepath))

        # Can we create an entry with the same name and date as an existing one?
        with self.assertRaises(argparse.ArgumentTypeError) as test_exception:
            entrymgr.create_entry(self._entry_title, self._entry_date)
        self.assertEqual(test_exception.exception.message,
            "Entry with filename '%s' exists." % target_filepath)

        # Can we delete the entry?
        entrymgr.delete_entry(self._entry_title, self._entry_date)

        # Is the file gone?
        self.assertFalse(os.path.isfile(target_filepath))

        # Is the entry's directory still around?
        self.assertFalse(os.path.isdir("2013/05/18"))

class ExpungeEmptyDirectoryTestCase(EntryMgrFakeJournalTestCase):
    # Test that expunging empty directories works.
    _entry_titles = ["Expunging test", "Post number 2"]
    _date_as_string = "2019/03/25"
    _entry_date = entrymgr.generate_datestamp(_date_as_string)

    def test_upward_delete_as_children_go(self):
        year, month, day = entrymgr.split_datestamp_string(self._date_as_string)

        # Create two entries for the same date.
        for title in self._entry_titles:
            entrymgr.create_entry(title, self._entry_date)

        for title in self._entry_titles:
            self.assertEqual(
                    len(os.listdir(self._date_as_string)),
                    len(self._entry_titles) - self._entry_titles.index(title))
            self.assertTrue(os.path.isdir(self._date_as_string))
            entrymgr.delete_entry(title, self._entry_date)

        self.assertFalse(os.path.isdir(self._date_as_string))
        self.assertFalse(os.path.isdir("%s/%s" % (year, month)))
        self.assertFalse(os.path.isdir("%s" % year))

    def test_directory_with_children_unremovable(self):
        year, month, day = entrymgr.split_datestamp_string(self._date_as_string)

        # Create two entries for the same date.
        for title in self._entry_titles:
            entrymgr.create_entry(title, self._entry_date)

        for title in self._entry_titles:
            if self._entry_titles.index(title) is 0:
                self.assertEqual(len(os.listdir(self._date_as_string)), 2)
                self.assertEqual(len(os.listdir("%s/%s" % (year, month))), 1)
                entrymgr.expunge_directory_if_empty(self._date_as_string)
                self.assertEqual(len(os.listdir(self._date_as_string)), 2)
                self.assertEqual(len(os.listdir("%s/%s" % (year, month))), 1)

    def test_different_months_removals(self):
        _entry_dates = [entrymgr.generate_datestamp("2013/05/16"),
                        entrymgr.generate_datestamp("2013/06/16"),
                        entrymgr.generate_datestamp("2013/07/16")]

        self._entry_titles.append("Third entry")

        for title in self._entry_titles:
            # Create three entries with the dates above.
            entrymgr.create_entry(title,
                _entry_dates[self._entry_titles.index(title)])

        # We have three entries with three different months in one year.
        self.assertEqual(len(os.listdir("2013")), 3)

        # Remove an entry.
        entrymgr.delete_entry(self._entry_titles[1], _entry_dates[1])

        # We should have two directories under '2013'.
        self.assertEqual(len(os.listdir("2013")), 2)

        # Third entry no longer required for tests.
        self._entry_titles.remove("Third entry")

class SplitDatestampStringTestCase(unittest.TestCase):
    def runTest(self):
        date = "2019/03/30"
        y, m, d = entrymgr.split_datestamp_string(date)

        self.assertItemsEqual([y, m, d], ["2019", "03", "30"])

class FormulateEntryFilenameTestCase(unittest.TestCase):
    def test_filename_always_lowercase(self):
        test_entry_name = "Title"

        result = entrymgr.formulate_entry_filename(test_entry_name)

        self.assertEqual(test_entry_name.lower() + ".md", result)

    def test_filename_spaces_are_dashes(self):
        test_entry_name = "Jackie Cane"

        result = entrymgr.formulate_entry_filename(test_entry_name)

        self.assertEqual("jackie-cane.md", result)

    def test_filename_extension_exists(self):
        test_entry_name = "Dirty Lenses"

        result = entrymgr.formulate_entry_filename(test_entry_name)

        self.assertEqual(result[-3:], '.md')

    def test_filename_entry_name_not_none(self):
        test_entry_name = ""

        with self.assertRaises(ValueError) as test_exception:
            result = entrymgr.formulate_entry_filename(test_entry_name)
