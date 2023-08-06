#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018, 2019, 2020 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>


import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/" + "../"))
import citellusclient.shell as citellus

testplugins = os.path.join(citellus.citellusdir, "plugins", "test")
citellusdir = citellus.citellusdir


class CitellusTest(TestCase):
    def test_plugins_have_dual_brackets_for_if(self):
        pluginpath = [os.path.join(citellus.citellusdir, "plugins", "core")]
        pluginscit = []
        for plugin in citellus.findplugins(folders=pluginpath):
            filename = plugin["plugin"]
            regexp = r"if \[ "
            if citellus.regexpfile(filename=filename, regexp=regexp):
                pluginscit.append(filename)

        assert len(pluginscit) == 0

    def test_plugins_have_dual_parenthesis_for_if(self):
        pluginpath = [os.path.join(citellus.citellusdir, "plugins", "core")]
        pluginscit = []
        for plugin in citellus.findplugins(folders=pluginpath):
            filename = plugin["plugin"]
            regexp = r"if \( "
            if citellus.regexpfile(filename=filename, regexp=regexp):
                pluginscit.append(filename)

        assert len(pluginscit) == 0
