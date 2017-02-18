#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(Unnoficial) Waf Conan Generator

See README at (https://github.com/paulobrizolara/waf-conangenerator) for instructions.

"""

from conans import ConanFile

class WafGeneratorPackage(ConanFile):
    name        = "WafGenerator"
    version     = "0.0.3"
    description = "Conan generator for waf projects. Allows including conan dependencies in wscripts."
    url         = "https://github.com/paulobrizolara/waf-conangenerator"
    author      = "Paulo Brizolara (paulobrizolara@tuta.io)"
    license     = "MIT"
    exports     = "waf_generator.py"

    def build(self):
      pass

    def package(self):
        pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []

from waf_generator import WafGenerator

class Waf(WafGenerator):
    def __init__(self, *k, **kwargs):
        super(Waf, self).__init__(*k, **kwargs)

