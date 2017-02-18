#!/usr/bin/env python
# -*- coding: utf-8 -*-

from waf_generator import WafGenerator

from conans import ConanFile
from conans.model.build_info import DepsCppInfo, CppInfo

import os
from os import path
import tempfile

class FakeConanFile(object):
    def __init__(self):
        self.deps_env_info  = {}
        self.env_info       = {}
        self.deps_cpp_info  = DepsCppInfo()
        self.cpp_info       = {}

def build_cpp_info(base_dir, **kw):
    cpp_info = CppInfo(base_dir)

    for attr, value in kw.items():
        setattr(cpp_info, attr, value)

    return cpp_info

class TestGenerator:
    foo = build_cpp_info('foo_dir',
            libs = ["foo"]
    )
    bar = build_cpp_info('bar_dir',
            libs = ["bar"],
            cppflags = ["-std=c++11"]
    )
    empty_conf = build_cpp_info('empty',
        libdirs = [],
        bindirs = [],
        includedirs = []
    )

    def setup_method(self, method):
        self.gen = WafGenerator(FakeConanFile())

    def teardown_method(self, method):
        pass

    def test_gen_content(self):
        self.add_dependency('bar', self.bar)
        self.add_dependency('foo', self.foo)
        self.add_dependency('empty', self.empty_conf)

        lines = [
            'def configure(conf):',
                '\t# bar',
                '\tconf.env.CXXFLAGS_bar=["-std=c++11"]',
                '\tconf.env.INCLUDES_bar=["{0}include"]',
                '\tconf.env.LIB_bar=["bar"]',
                '\tconf.env.LIBPATH_bar=["{0}lib"]',
                '\tconf.env.RPATH_bar=["{0}lib"]',
                '',
                '\t# foo',
                '\tconf.env.INCLUDES_foo=["{1}include"]',
                '\tconf.env.LIB_foo=["foo"]',
                '\tconf.env.LIBPATH_foo=["{1}lib"]',
                '\tconf.env.RPATH_foo=["{1}lib"]',
                '',
                ''
        ]

        bar_dir = "bar_dir" + os.sep
        foo_dir = "foo_dir" + os.sep

        expected_out='\n'.join(lines).format(bar_dir, foo_dir)

        assert self.gen.content == expected_out

    def test_gen_content_for_empty_dependencies(self):
        self.add_dependency('empty', self.empty_conf)

        lines = [
            'def configure(conf):',
                '\tpass'
        ]

        expected_out='\n'.join(lines)

        assert self.gen.content == expected_out


    def add_dependency(self, dep_name, deps):
        self.gen.deps_build_info._dependencies[dep_name] = deps
