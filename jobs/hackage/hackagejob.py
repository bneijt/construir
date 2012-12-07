#!/usr/bin/python
import os
import logging
import argparse
import sys
import subprocess
import shutil
import stat

NULL = file(os.path.devnull, "w")
EXEC_PERMS = stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXGRP | stat.S_IRGRP | stat.S_IXOTH | stat.S_IROTH
HP_VERSION = "2012.4.0.0"
def cabal(cmd):
    environment = os.environ.copy()
    environment["HOME"] = os.path.realpath("job/pkg")
    cp =  subprocess.Popen(cmd,
        stdin=subprocess.PIPE,
        cwd = os.path.join("job/pkg"),
        env = environment)
    cp.stdin.close()
    return cp

def searchAndReplaceInFile(s, r, f):
    smallTextFile = file(f, "r")
    newContent = smallTextFile.read().replace(s, r)
    smallTextFile.close()
    smallTextFile = file(f, "w+")
    smallTextFile.seek(0)
    smallTextFile.write(newContent)
    smallTextFile.truncate()
    smallTextFile.close()

def searchAndReplaceInCabalConfig(s, r):
    print("Rewriting configuration paths")
    searchAndReplaceInFile(s, r, "job/pkg/.cabal/config")

def main():
    if not os.path.exists("job"):
        print("This program needs to be run next to a job directory")
        print(" you can download a job directory archive from the")
        print(" construir project website")
        return 1
    parser = argparse.ArgumentParser(description='Create cabal job for construir')
    parser.add_argument('pkg_names',
                   help='The Hackage package name', nargs="+")
    config = parser.parse_args()
    for pkg_name in config.pkg_names:
        print("=== " + pkg_name + " ===")
        if os.path.exists("job/pkg"):
            shutil.rmtree("job/pkg")
        os.mkdir("job/pkg")
        cp = cabal(["cabal", "update"])
        cp.communicate()
        cp.wait()
        cp = cabal(["cabal", "fetch", pkg_name])
        cp.communicate()
        cp.wait()
        #Rewrite cabal configuration root
        localPath = os.path.realpath("job/pkg")
        buildserverPath = "/root"
        searchAndReplaceInCabalConfig(localPath, buildserverPath)
        if not os.path.exists("job/bin"):
            os.mkdir("job/bin")
        if os.path.exists("job/bin/construir"):
            os.unlink("job/bin/construir")
        shutil.copy("construir.template", "job/bin/construir")
        os.chmod("job/bin/construir", EXEC_PERMS)
        searchAndReplaceInFile("PKGNAME", pkg_name, "job/bin/construir")
        searchAndReplaceInFile("HP_VERSION", HP_VERSION, "job/bin/construir")
        print("Running mkjob.py")
        rstatus = subprocess.call(["../mkjob.py", "--extra-space", "1000", "job"])
        assert rstatus == 0
        os.rename("job.ext2", pkg_name + ".ext2")
        return 0

if __name__ == "__main__":
    sys.exit(main())


