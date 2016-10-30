#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conans
from conans.model import Generator
from collections import OrderedDict

class WafGenerator(Generator):
    NAMES_MAP = {
        'include_paths' : 'INCLUDES',
        'lib_paths'     : 'LIBPATH',
        'bin_paths'     : '',
        'libs'          : 'LIB',
        'defines'       : 'DEFINES',
        'cflags'        : 'CFLAGS',
        'cppflags'      : 'CXXFLAGS',
        'sharedlinkflags' : 'LINKFLAGS',
        'exelinkflags' : '',
    }

    def __init__(self, *k, **kwargs):
        super(WafGenerator, self).__init__(*k, **kwargs)

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

        counter = 0
        if wafConfigs:
            for depName, deps in wafConfigs.iteritems():
                counter += self.write_dep(depName, deps, file_str)

        if not counter: # No configuration writed
            file_str.write("\tpass")

        return file_str.getvalue()

    def write_dep(self, depName, depProperties, out):
        if not depProperties: #empty
            return 0

        out.write("\t# %s\n" % depName)

        for key, value in depProperties.iteritems():
            out.write("\tconf.env.")
            out.write(key)
            out.write('=[')

            #Require that value be an list
            valuesList = [('"'+ v + '"') for v in value]
            out.write(", ".join(valuesList))
            out.write(']\n')

        out.write('\n')

        return 1

    def genConfigs(self):
        wafConfigs = OrderedDict()

        depsInfo = self.deps_build_info

        for depName in depsInfo.deps:
            dep = depsInfo[depName]
            self.addDependency(depName, dep, wafConfigs)

            if self.gen_rpaths and dep.lib_paths:
                prop = [self.makePropertyName('RPATH', depName), dep.lib_paths]
                self.addProp(depName, prop, wafConfigs)

        return wafConfigs

    def addDependency(self, depName, dep, wafConfigs):
        wafConfigs[depName] = OrderedDict()

        for attr in self.NAMES_MAP:
            self.addProperty(attr, depName, dep, wafConfigs)

    def addProperty(self, attr, depName, dep, wafConfigs):
        prop = self.makeProperty(attr, depName, getattr(dep, attr))

        self.addProp(depName, prop, wafConfigs)

    def addProp(self, depName, prop, wafConfigs):
        if prop:
            wafConfigs[depName][prop[0]] = prop[1]

    def makeProperty(self, prop, depName, depValue):
        if not self.NAMES_MAP[prop] or not depValue:
            return None

        propName = self.makePropertyName(self.NAMES_MAP[prop], depName)

        return (propName, depValue)

    def makePropertyName(self, propName, dependencyName):
        return propName + '_' + dependencyName.replace('-', '_')
