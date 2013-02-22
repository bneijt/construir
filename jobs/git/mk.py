#!/usr/bin/python3
import os
import subprocess
import argparse
import sys

class otherCwd:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.oldPath = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.oldPath)


def start(args, workingDirectory):
    cp =  subprocess.Popen(cmd,
        stdin=subprocess.PIPE,
        cwd = workingDirectory)
    cp.stdin.close()
    return process.wait()

def main():
 
    parser = argparse.ArgumentParser(description='Build construir from git repo checkout')
    parser.add_argument("--pull", help = "Perform a git pull before job creation", action="store_true")

    config = parser.parse_args()

    if not os.path.exists("repo"):
        print("You have to make a checkout of your repository in a directory named repo")
        print("For example: git clone git://somewhere/something.git repo")
        return 1
    if config.pull:
        with otherCwd("repo"):
            subprocess.call(["git", "pull"])

    if not os.path.exists("repo/construir"):
        print ("You have to have a construir script in your repo")
        print ("Was looking at: repo/construir")
        return 1
    #Extract git tag information and project information to create job filename
    jobName = None
    with otherCwd("repo"):
        gitRev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8", "ignore").strip()
        gitRemote = subprocess.check_output(["git", "config", "--local", "--get", "remote.origin.url"]).decode("utf-8", "ignore").strip()
        if gitRemote.endswith("/"):
            gitRemote = gitRemote[:-1]
        jobName = "%s_%s" % (os.path.basename(gitRemote), gitRev)
        jobName = jobName.replace("/", "")
    assert jobName != None
    jobFileName = jobName + "_i1.tar.xz"
    subprocess.call(["tar", "--verbose", "--create", "--xz", "--exclude=.git", "--file", jobFileName, "repo", "job"])
    if os.path.getsize(jobFileName) < 512000:
        subprocess.call(["truncate", "--size=500K", jobFileName])
    return 0

if __name__ == "__main__":
    sys.exit(main())
