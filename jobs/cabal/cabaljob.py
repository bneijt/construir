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
CABAL_PATH = "root"
CABAL_CONFIG = os.path.join(CABAL_PATH, ".cabal", "config")
CABAL_CONFIG_ORIG = CABAL_CONFIG + ".orig"

GIT_REPO = "job/repo"

def cabal(cmd):
    environment = os.environ.copy()
    environment["HOME"] = os.path.realpath(CABAL_PATH)
    cp =  subprocess.Popen(cmd,
        stdin=subprocess.PIPE,
        cwd = os.path.join(GIT_REPO),
        env = environment)
    cp.stdin.close()
    return cp

def searchAndReplaceInFile(s, r, f):
    smallTextFile = file(f, "r")
    oldContent = smallTextFile.read()
    newContent = oldContent.replace(s, r)
    smallTextFile.close()
    smallTextFile = file(f, "w+")
    smallTextFile.seek(0)
    smallTextFile.write(newContent)
    smallTextFile.truncate()
    smallTextFile.close()

def searchAndReplaceInCabalConfig(s, r):
    print("Rewriting configuration paths")
    searchAndReplaceInFile(s, r, CABAL_CONFIG)

def main():
    if not os.path.exists("job"):
        print("This program needs to be run next to a job directory")
        return 1

    parser = argparse.ArgumentParser(description='Create cabal job for construir')
    parser.add_argument("--fresh", help = "Remove existing .cabal configuration", action="store_true")
    parser.add_argument('git_url',
                   help='The git url to clone from')
    config = parser.parse_args()
    #Clone from git_url
    if os.path.exists(GIT_REPO):
        shutil.rmtree(GIT_REPO)
    cp =  subprocess.Popen(["git", "clone", config.git_url, GIT_REPO],
        stdin = subprocess.PIPE,
        stdout = file("job/git_clone.txt", "w"))
    cp.stdin.close()
    cp.communicate()
    cp.wait()
    if not os.path.exists("root"):
        os.mkdir("root")
    if config.fresh or (not os.path.exists(CABAL_CONFIG_ORIG)):
        if os.path.exists(CABAL_PATH):
            shutil.rmtree(CABAL_PATH)
        os.mkdir(CABAL_PATH)

        os.mkdir(CABAL_PATH + "/.cabal")

        cp = cabal(["cabal", "update"])
        cp.communicate()
        assert cp.wait() == 0

        #Keep original configuration file
        shutil.copyfile(CABAL_CONFIG, CABAL_CONFIG_ORIG)

    #To fetch, we need the original configuration file
    shutil.copyfile(CABAL_CONFIG_ORIG, CABAL_CONFIG)
    cp = cabal(["cabal", "fetch", "."])
    cp.communicate()
    assert cp.wait() == 0

    #Rewrite cabal configuration root
    localPath = os.path.realpath(CABAL_PATH)
    buildserverPath = "/root"
    searchAndReplaceInCabalConfig(localPath, buildserverPath)

    jobName = os.path.basename(os.path.realpath(config.git_url))
    gitRev = subprocess.check_output(["git", "--git-dir", os.path.join(GIT_REPO, ".git"), "rev-parse", "--short", "HEAD"]).decode("utf-8", "ignore").strip()
    jobFileName = "%s_%s_i1.tar.xz" % (jobName, gitRev)
    subprocess.call(["tar", "--verbose", "--create", "--xz", "--exclude=.git", "--file", jobFileName, "job", "root"])
    if os.path.getsize(jobFileName) < 512000:
        subprocess.call(["truncate", "--size=500K", jobFileName])

    return 0

if __name__ == "__main__":
    sys.exit(main())


