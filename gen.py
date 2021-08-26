
import os
import subprocess
import json

conanfile_content = r'''[requires]
fmt/6.1.2

[generators]
json'''

if not os.path.exists("tmp"):
    os.makedirs("tmp")

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
    print("finish")


add_requires("hello")