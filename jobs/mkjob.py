#!/usr/bin/python
import os
import logging
import argparse
import sys
import subprocess

NULL = file(os.path.devnull, 'w')
MB = 1024 #Blocks
GB = 1024*MB

def genext2fs_available():
    try:
        subprocess.call(["genext2fs", "--version"], stdout=NULL, stderr=NULL)
        return True
    except Exception, e:
        return False

class Job:
    def __init__(self, path):
        self.path = os.path.normpath(path)
        self.image = None

    def setOutputImage(self, outputImage):
        self.image = outputImage

    def size(self):
        '''Size for this job image'''
        return self.jobSize() + self.extraSpace

    def setExtraSpace(self, size):
        self.extraSpace = size

    def jobSize(self):
        total = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            total += sum([os.path.getsize(os.path.join(dirpath, f)) for f in filenames])
            total += os.path.getsize(dirpath)
        return (total / 1024)

    def basename(self):
        return os.path.basename(self.path)

    def gen(self):
        assert self.image
        assert self.path
        assert os.path.exists(self.path)
        cmd = ['genext2fs', '--root', self.path, '--size-in-blocks', str(self.size()), self.image]
        status = subprocess.call(cmd, stdout=NULL, stderr=NULL)
        return status == 0

    def __str__(self):
        return "Job '%s' -> '%s'" %(self.path, self.image)

def main():
    parser = argparse.ArgumentParser(description='Create construir job images from a directory')
    parser.add_argument('job_directory',
                   help='The directory to create a job image from')
    parser.add_argument('--extra-space', dest="extra_space",
                   default=10, type=int,
                   help='The number of extra megabytes needed in image')

    config = parser.parse_args()
    if not os.path.exists(config.job_directory):
        logging.error("Given job directory '%s' does not exist" % config.job_directory)
        return 1
    if not os.path.isdir(config.job_directory):
        logging.error("Directory argument '%s' is not a directory" % config.job_directory)
    if not genext2fs_available():
        logging.error("Could not find genext2fs to create image")
        return 1
    construirScript = os.path.join(config.job_directory, 'bin', 'construir')
    if not os.path.exists(construirScript):
        logging.error("Job directory did not contain construir script")
        logging.error("Missing file '%s'" % construirScript)
        return 1

    #Calculate job size
    job = Job(config.job_directory)
    job.setOutputImage(job.basename() + ".ext2")
    job.setExtraSpace(config.extra_space * 1024)
    job.gen()



if __name__ == "__main__":
    sys.exit(main())


