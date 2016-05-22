#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, ConfigureEnvironment
import os

class PocoTimerConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "Poco/1.7.2@lasote/stable" ,

        "WafGenerator/0.0.1@paulobrizolara/experimental"
    )

    generators = "Waf"
    default_options = "Poco:shared=True", "OpenSSL:shared=True"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin") # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        os.chdir(self.conanfile_directory)
        waf = os.path.join(self.conanfile_directory, 'waf')
        self.run('%s configure build' % waf)

    def test(self):
        pass
