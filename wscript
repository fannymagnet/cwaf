#! /usr/bin/env python
# encoding: utf-8

import os
import subprocess
import json

conanfile_content = r'''[requires]
fmt/6.1.2

[generators]
json'''

if not os.path.exists("tmp"):
    os.makedirs("tmp")

include_dirs = ['.']
lib_dirs = []

def add_requires(package):
    with open("tmp/conanfile.txt", 'w') as f: 
        f.write(conanfile_content)

    os.chdir("tmp")
    cmd = "conan install . --build=missing"
    subprocess.run(cmd)

    with open("conanbuildinfo.json") as f:
        data = json.loads(f.read())
        deps = data["dependencies"]
        for dep in deps:
            print(dep["name"])
            pkg_include_dirs = dep['include_paths']
            for pkg_include_dir in pkg_include_dirs:
                include_dirs.append(pkg_include_dir)
                
            pkg_lib_dirs = dep['lib_paths']
            for pkg_lib_dir in pkg_lib_dirs:
                lib_dirs.append(pkg_lib_dir)
    print("finish")

def options(opt):
    opt.load('compiler_cxx')

def configure(conf):
    conf.setenv('release')
    conf.load('compiler_cxx')

def build(bld):
    add_requires('fmt')
    bld.program(
        source='main.cpp',
        target='app',

        includes=include_dirs,
        libpath=lib_dirs,
        lib=['fmt'],
    )