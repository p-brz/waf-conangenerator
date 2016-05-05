#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(Unnoficial) Waf Conan Generator

See README for instructions.

"""

from conans import ConanFile

from WafGenerator import *

class WafGeneratorPackage(ConanFile):
    name = "WafGenerator"
    version = "0.0.1"
    url = "https://github.com/paulobrizolara/waf-conangenerator"
    author = "Paulo Leonardo Souza Brizolara (souzabrizolara@gmail.com)"'
    license = "MIT"
    exports = "*.py"

    def build(self):
      pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []

#Workaround to allow put WafGenerator on other file
class Waf(WafGenerator):
    pass
