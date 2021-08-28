#! /usr/bin/env python
# encoding: utf-8

import re
import os
import subprocess
import json

class Package:
    def __init__(self) -> None:
        self.manager = ""
        self.name = ""
        self.version = ""


    def toString(self):
        print('package manager:' + self.manager)
        print('package name:' + self.name)
        print('package version:' + self.version)


class PackageRepo:
    def __init__(self) -> None:
        self.packages = {}
        self.include_dirs = []
        self.lib_dirs = []
        self.stlibs = []
        self.shlibs = []

    def installPackages(self, packages):
        pass


class PackageManager:
    def __init__(self) -> None:
        self.package_repos = {}
        self.packages = {}
        self.include_dirs = ['.']
        self.lib_dirs = ['.']
        self.stlibs = []
        self.shlibs = []
        self.add_package_repo("conan", ConanRepo)


    def add_package_repo(self, name, repo_type):
        self.package_repos[name] = repo_type()


    def add_requires(self, *args):
        pkgs = []
        for arg in args:
            match_result = re.match(r'(.*)::(.*)/(.*)', arg)
            pkg = Package()
            pkg.manager = match_result.group(1)
            pkg.name = match_result.group(2)
            pkg.version = match_result.group(3)
            pkgs.append(pkg)

        self.addPackages(pkgs)
        # TODO: call this in the end
        self.installPackages()


    def addPackage(self, package):
        if package.manager in self.packages:
            self.packages[package.manager].append(package)
        else:
            self.packages[package.manager] = [package]


    def addPackages(self, packages):
        for package in packages:
            self.addPackage(package)


    def installPackages(self):
        for k, v in self.packages.items():
            if k in self.package_repos:
                repo = self.package_repos[k]
                repo.installPackages(v)
                for include_dir in repo.include_dirs:
                    self.include_dirs.append(include_dir)
                for lib_dir in repo.lib_dirs:
                    self.lib_dirs.append(lib_dir)
                for stlib in repo.stlibs:
                    self.stlibs.append(stlib)
                for shlib in repo.shlibs:
                    self.shlibs.append(shlib)
            else:
                print("unsupported packaged manager: " + k)
                continue


class ConanRepo(PackageRepo):
    def __init__(self) -> None:
        PackageRepo.__init__(self)


    def installPackages(self, packages):
        # gen conanfile.txt
        conanfile_content = '[requires]\n'
        for package in packages:
            conanfile_content += package.name + '/' + package.version + '\n'
        conanfile_content += '[generators]\njson'
        print(conanfile_content)
        self.installConanPackages(conanfile_content)


    def installConanPackages(self, conanfile_content):
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        os.curdir = os.getcwd()
        os.chdir('tmp')
        with open('conanfile.txt', 'w') as f: 
            f.write(conanfile_content)

        cmd = "conan install . --build=missing"
        subprocess.run(cmd)

        with open('conanbuildinfo.json') as f:
            data = json.loads(f.read())

            options = data['options']

            deps = data['dependencies']
            for dep in deps:
                print(dep['name'])
                pkg_include_dirs = dep['include_paths']
                for pkg_include_dir in pkg_include_dirs:
                    self.include_dirs.append(pkg_include_dir)
                    
                pkg_lib_dirs = dep['lib_paths']
                for pkg_lib_dir in pkg_lib_dirs:
                    self.lib_dirs.append(pkg_lib_dir)

                pkg_libs = dep['libs']
                for pkg_lib in pkg_libs:
                    if options[pkg_lib]['shared'] == 'False':
                        self.stlibs.append(pkg_lib)
                    else:
                        self.shlibs.append(pkg_lib)

        os.chdir(os.curdir)
        print("install conan packages finished")

