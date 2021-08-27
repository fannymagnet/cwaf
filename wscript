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
    app = bld.program(
        source = 'main.cpp',
        target = 'app',
        includes = pkg_mgr.include_dirs,
        stlibpath = pkg_mgr.lib_dirs,
        stlib = pkg_mgr.stlib,
        shlib = pkg_mgr.shlib
    )

    if bld.env.CC_NAME == 'msvc':
        app.cxxflags = ['/MD']