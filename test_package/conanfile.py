#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, ConfigureEnvironment
import os

name     = "WafGenerator"
version  = "0.0.3"
username = os.getenv("CONAN_USERNAME", "paulobrizolara")
channel  = os.getenv("CONAN_CHANNEL", "testing")

class ExampleConanFile(ConanFile):
    build_policy = "missing"
    settings = "os", "compiler", "build_type", "arch"
    
    requires = (
        "%s/%s@%s/%s" % (name, version, username, channel),
        
        "Hello/0.1@memsharded/testing",
    )

    generators = "Waf"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin") # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        waf = os.path.join(".", "waf")
        self.run("'%s' configure build -o '%s'" % (waf, os.getcwd()), cwd=self.conanfile_directory)

    def test(self):
        self.run("pwd")
        self.run(os.path.join(".", "example"))
