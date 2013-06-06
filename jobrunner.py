#!/usr/bin/python
import os
import pyinotify
import threading
import Queue
import subprocess
import time
import logging
import datetime
import argparse
import re
import io

import binascii

NULL = file(os.path.devnull, 'w')
MINUTES = 60
MAXIMUM_JOB_TIME = 30 * MINUTES
wm = pyinotify.WatchManager()
jobQueue = Queue.Queue()

#TODO
def trimTrailingZeroBytesOf(path):
    '''Trim all the zero bytes at the end of a file'''
    BLOCK_SIZE = 1024
    f = file(path, 'r+b')
    lastNonZeroIndex = 0
    while True:
        blockPosition = f.tell()
        block = f.read(BLOCK_SIZE)
        if not block:
            break
        for idx in range(block
        for i in block:
            if i != '\x00':
                lastNonZeroIndex = f.tell()
    f.truncate(lastNonZeroIndex)
    f.close()


class JobLogger:
    def __init__(self, jobName):
        self.jobName = str(jobName)
        self.logger = logging.getLogger('joblogger')
    def info(self, msg):
        self.logger.info("[%s] %s" % (self.jobName, msg))
    def debug(self, msg):
        self.logger.debug("[%s] %s" % (self.jobName, msg))
    def warn(self, msg):
        self.logger.warn("[%s] %s" % (self.jobName, msg))
    def error(self, msg):
        self.logger.error("[%s] %s" % (self.jobName, msg))

class Job:
    imageNumberPattern = re.compile("_i([0-9]+)\\.tar\\.xz")

    def __init__(self, path):
        self.path = path
        self.size = os.path.getsize(path)
    def changed(self):
        return self.size != os.path.getsize(self.path)
    def imageNumber(self):
        matchingJob = Job.imageNumberPattern.search(self.path)
        if matchingJob != None:
            return matchingJob.group(1)
        return None
    def doneName(self):
        basename = os.path.basename(self.path)
        return Job.imageNumberPattern.sub("_d\\1.tar.xz", basename)


class JobRunner(threading.Thread):
    vmProcess = None
    currentJob = None
    runningJobPath = "job.tar.xz"

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.logger = JobLogger(None)
        self.config = config

    def switchJob(self):
        jobName = "None"
        if self.currentJob:
            jobName = str(self.currentJob.path)
        self.logger.debug("Switching to " + jobName)
        self.logger = JobLogger(jobName)

    def waitForEndOfRunningJob(self):
        if self.vmProcess != None:
            self.logger.info("Waiting for job to finish")
            timeout = time.time() + MAXIMUM_JOB_TIME
            while self.vmProcess.returncode == None and time.time() < timeout:
                #TODO Use vmProcess.wait(timeout=20) when 3.3 has hits the debian servers
                self.vmProcess.poll()
                time.sleep(10)
            if self.vmProcess.returncode == None:
                self.logger.warn("Killing job")
                self.vmProcess.kill()
            self.logger.info("End")
            self.vmProcess = None

    def startJob(self):
        self.logger.info("Start")

        os.rename(self.currentJob.path, self.runningJobPath)
        assert os.path.exists(self.runningJobPath)
        #Determine the image it should run with
        #Determine image name
        requestedImage = self.currentJob.imageNumber()
        if requestedImage == None:
            self.logger.info("No image spec found in job name, skipping")
            return
        requestedImagePath = os.path.join(self.config.image, "i" + requestedImage + ".qcow2")
        if not os.path.exists(requestedImagePath):
            self.logger.error("Requested image %s not found" % requestedImagePath)
            return
        assert os.path.exists(requestedImagePath)
        args = [
            "/usr/bin/kvm",
            "-no-fd-bootchk",
            "-nographic",
            "-enable-kvm",
            "-no-reboot",
            "-m", "512M",
            "-drive",
            "file=" + requestedImagePath + ",index=0,media=disk,snapshot=on",
            "-drive",
            "file=" + self.runningJobPath + ",index=1,media=disk,format=raw"]
        if not self.config.enable_networking:
            args.extend(["-net", "none"])
        self.vmProcess = subprocess.Popen(args, 
            stdin=None, stdout=NULL, stderr=subprocess.STDOUT,
            close_fds=True)
        self.logger.info("Started with pid %i" % self.vmProcess.pid)

    def saveJobImage(self):
        assert self.currentJob
        #trimTrailingZeroBytesOf(self.runningJobPath)
        outputName = self.currentJob.doneName()
        self.logger.info("Saving output to: " + outputName)
        outputPath = os.path.join(self.config.done, outputName)
        os.rename(self.runningJobPath, outputPath)
        assert not os.path.exists(self.runningJobPath)

    def moveJobToDone(self):
        assert self.vmProcess == None
        self.logger.info("Moving job to done")
        if os.path.exists(self.runningJobPath):
            if self.currentJob != None:
                self.saveJobImage()
            self.currentJob = None
            self.switchJob()

    def run(self):
        self.logger.info("Jobrunner started")
        #First run, wait for a job and start server
        while True:
            try:
                self.currentJob = jobQueue.get(True)
                if self.currentJob == None:
                    break
                self.switchJob()
                if not os.path.exists(self.currentJob.path):
                    self.logger.warn("File missing, skipping job")
                    continue
                if self.currentJob.changed():
                    self.logger.warn("Job file changed in transit, skipping job")
                    continue
                self.startJob()
                self.waitForEndOfRunningJob()
                self.moveJobToDone()
            except Exception, e:
                self.logger.error("Caught exception: " +  str(e))
        self.logger.info("Jobrunner ended")


class QueueEventHandler(pyinotify.ProcessEvent):
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_MOVED_TO
    def __init__(self, config):
        pyinotify.ProcessEvent(self)
        self.config = config

    def process_IN_CLOSE_WRITE(self, event):
        if event.name:
            self.verifyAndQueue(event.name)
    def process_IN_CLOSE_NOWRITE(self, event):
        if event.name:
            self.verifyAndQueue(event.name)
    def process_IN_MOVED_TO(self, event):
        if event.name:
            self.verifyAndQueue(event.name)

    def verifyAndQueue(self, jobName):
        logging.info("Adding job to queue: %s", jobName)
        jobQueue.put(Job(os.path.join(self.config.queue, jobName)))

def main():
    os.nice(10)
    parser = argparse.ArgumentParser(description='Run construir jobs entered into the queue directory')
    parser.add_argument("--queue", help = "Directory to queue", default = "./queue")
    parser.add_argument("--done", help = "Directory to store finalized jobs", default = "./done")
    parser.add_argument("--image", help = "Directory containing images", default = "./image")
    parser.add_argument("--enable-networking", help = "Allow the job to access the network. Enable only on trusted job queues!", action="store_true")

    config = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    if not os.path.exists(config.done):
        os.mkdir(config.done)
    if not os.path.exists(config.queue):
        os.mkdir(config.queue)

    jr = JobRunner(config)
    jr.start()
    notifier = pyinotify.Notifier(wm, QueueEventHandler(config))
    wdd = wm.add_watch(config.queue, QueueEventHandler.mask , rec=False)
    notifier.loop()
    jobQueue.put(None)
    logging.info("Joining with jobrunner")
    if jr.isAlive():
        jr.join()



if __name__ == "__main__":
    main()

