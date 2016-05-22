#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(Unnoficial) Waf Conan Generator

See README for instructions.

"""

from conans import ConanFile

class WafGeneratorPackage(ConanFile):
    name = "WafGenerator"
    version = "0.0.1"
    url = "https://github.com/paulobrizolara/waf-conangenerator"
    author = "Paulo Leonardo Souza Brizolara (souzabrizolara@gmail.com)"
    license = "MIT"
    settings = None

    def build(self):
      pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []

from conans.model import Generator

class Waf(Generator):
    NAMES_MAP = {
        'include_paths' : 'INCLUDES',
        'lib_paths'     : 'LIBPATH',
        'bin_paths'     : '',
        'libs'          : 'LIB',
        'defines'       : 'DEFINES',
        'cflags'        : 'CFLAGS',
        'cppflags'      : 'CXXFLAGS',
        'sharedlinkflags' : 'LINKFLAGS',
        'exelinkflags' : ''
    }

    def __init__(self, *k, **kwargs):
        super(Waf, self).__init__(*k, **kwargs)

        self.gen_rpaths = True

    @property
    def filename(self):
        return "conanbuildinfo_waf.py"

    @property
    def content(self):
        return self.genWafFile(self.genConfigs())

    def genWafFile(self, wafConfigs):
        from cStringIO import StringIO
        file_str = StringIO()
        file_str.write("def configure(conf):\n")

        for key, value in wafConfigs.iteritems():
            file_str.write("\tconf.env.")
            file_str.write(key)
            file_str.write('=[')

            #Require that value be an list
            valuesList = [('"'+ v + '"') for v in value]
            file_str.write(", ".join(valuesList))
            file_str.write(']\n')

        return file_str.getvalue()

    def genConfigs(self):
        wafConfigs = {}

        depsInfo = self.deps_build_info

        for depName in depsInfo.deps:
            dep = depsInfo[depName]
            self.addDependency(depName, dep, wafConfigs)

            if self.gen_rpaths and dep.lib_paths:
                prop = self.makePropertyName('RPATH', depName)
                wafConfigs[prop] = dep.lib_paths

        return wafConfigs

    def addDependency(self, depName, dep, wafConfigs):
        for attr in self.NAMES_MAP:
            self.addProperty(attr, depName, dep, wafConfigs)

    def addProperty(self, attr, depName, dep, wafConfigs):
        prop = self.makeProperty(attr, depName, getattr(dep, attr))

        if prop:
            wafConfigs[prop[0]] = prop[1]

    def makeProperty(self, prop, depName, depValue):
        if not self.NAMES_MAP[prop] or not depValue:
            return None

        propName = self.makePropertyName(self.NAMES_MAP[prop], depName)

        return (propName, depValue)

    def makePropertyName(self, propName, dependencyName):
        return propName + '_' + dependencyName.replace('-', '_')

