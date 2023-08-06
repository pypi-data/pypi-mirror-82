#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Robin Černín <cerninr@gmail.com>
# Copyright (C) 2017 Lars Kellogg-Stedman <lars@redhat.com>
# Copyright (C) 2017, 2018, 2019, 2020 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>

import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/" + "../"))
import citellusclient.shell as citellus

testplugins = os.path.join(citellus.citellusdir, "plugins", "test")
citellusdir = citellus.citellusdir


class CitellusTest(TestCase):
    def test_parseargs(self):
        # Call with no arguments
        try:
            citellus.parse_args()
        except:
            pass
        assert True

    def test_findplugins_positive_filter_include(self):
        plugins = citellus.findplugins([testplugins], include=["exit_passed"])

        assert len(plugins) == 1

    def test_findplugins_positive_filter_exclude(self):
        plugins = citellus.findplugins(
            [testplugins], exclude=["exit_passed", "exit_skipped"]
        )

        for plugin in plugins:
            assert "exit_passed" not in plugin and "exit_skipped" not in plugin

    def test_findplugins_positive(self):
        assert len(citellus.findplugins([testplugins])) != 0

    def test_findplugins_negative(self):
        assert citellus.findplugins("__does_not_exist__") == []

    def test_which(self):
        assert citellus.which("/bin/sh") == "/bin/sh"

    def test_findplugins_ext(self):
        plugins = []
        folder = [os.path.join(citellus.citellusdir, "plugins", "core")]
        for each in citellus.findplugins(
            folders=folder, fileextension=".sh", include=[".sh"], exclude=["potato"]
        ):
            plugins.append(each)
        assert len(plugins) != 0

    def test_readconfig(self):
        parsed = citellus.read_config()
        assert parsed == {}

    def test_main(self):
        sys.argv = ["citellus.py", "--list-plugins", "--list-categories"]
        try:
            citellus.main()
        except:
            pass
        assert True

    def test_help(self):
        sys.argv = ["citellus.py", "--help"]
        try:
            citellus.main()
        except:
            pass

        assert True
