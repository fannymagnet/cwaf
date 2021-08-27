#! /usr/bin/env python
# encoding: utf-8

import package

def options(opt):
    opt.load('compiler_cxx')

def configure(conf):
    # conf.setenv('release')
    conf.load('compiler_cxx')

def build(bld):
    pkg_mgr = package.PackageManager()
    pkg_mgr.add_requires('conan::fmt/6.1.2')
    # bld.read_stlib('fmt', paths=lib_dirs)
    app = bld.program(
        source='main.cpp',
        target='app',

        # use = "fmt", read_stlib can use this
        includes=pkg_mgr.include_dirs,
        stlibpath=pkg_mgr.lib_dirs,
        stlib=['fmt'],
    )

    if bld.env.CC_NAME == 'msvc':
        app.cxxflags = ['/MD']