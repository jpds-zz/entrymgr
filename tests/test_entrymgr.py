#!/usr/bin/python
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

import datetime
import os
import shutil
import sys
import unittest

sys.path.append("..")

import entrymgr

class EnsureDirectoryExists(unittest.TestCase):
    # Test our entrymgr.ensure_directory_exists() function works.
    _date = "2013/09/23"
    _target_test_directory = "tests/fakediary/"

    def runTest(self):
        # Create the directory structure based on the fake date above.
        entrymgr.ensure_directory_exists(
            self._target_test_directory + self._date)

        self.assertTrue(os.path.isdir(
            self._target_test_directory + self._date))

    def tearDown(self):
        # Remove the above directory.
        shutil.rmtree(self._target_test_directory)

        self.assertFalse(os.path.isdir(
            self._target_test_directory + self._date))

class FormulateDateStructureTestCase(unittest.TestCase):
    # Make sure that we create proper strings.
    def runTest(self):
        fake_date = datetime.datetime(2013, 9, 23)
        function_result = entrymgr.formulate_directory_structure(fake_date)
        self.assertEqual(function_result, "2013/09/23")

class CheckLicenseTestCase(unittest.TestCase):
    # Simple dummy test to ensure that even unittest is working.
    def runTest(self):
        self.assertEqual(entrymgr.__license__, "BSD")

class GenerateDatestampTestCase(unittest.TestCase):
    # Ensure that we can generate valid datestamps for entry directories.
    def runTest(self):
        control = datetime.datetime(2013, 9, 23)
        date = entrymgr.generate_datestamp("2013/09/23")
        self.assertEqual(date, control)

class EntryLifeCycleTestCase(unittest.TestCase):
    # Ensure that we can create an entry.
    _entry_title = "Testing Lifecycle"
    _entry_date = entrymgr.generate_datestamp("2013/09/23")
    _target_result = "Testing Lifecycle\n================="

    def runTest(self):
        # Create a fake directory and move our tests there.
        entrymgr.ensure_directory_exists("tests/fakediary")
        os.chdir("tests/fakediary")

        entrymgr.create_entry(self._entry_title, self._entry_date)

        entry_text = open("2013/09/23/testing-lifecycle.md", 'r').read()

        self.assertEqual(entry_text, self._target_result)

        self.assertTrue(os.path.isfile("2013/09/23/testing-lifecycle.md"))

        entrymgr.delete_entry(self._entry_title, self._entry_date)

        self.assertFalse(os.path.isfile("2013/09/23/testing-lifecycle.md"))
        self.assertTrue(os.path.isdir("2013/09/23"))

    def tearDown(self):
        # Remove the above directory.
        os.chdir("..")
        shutil.rmtree("fakediary")
