#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, ConfigureEnvironment
import os

name     = "WafGenerator"
version  = "0.0.2"
username = os.getenv("CONAN_USERNAME", "paulobrizolara")
channel  = os.getenv("CONAN_CHANNEL", "testing")

class PocoTimerConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "Poco/1.7.3@lasote/stable" ,

        "%s/%s@%s/%s" % (name, version, username, channel),
    )

    generators = "Waf"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin") # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        waf = os.path.join(".", "waf")
        self.run("'%s' configure build -o '%s'" % (waf, os.getcwd()), cwd=self.conanfile_directory)

    def test(self):
        pass
