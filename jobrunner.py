#!/usr/bin/python
import os
import pyinotify
import threading
import Queue
import subprocess
import time
import logging
import datetime

wm = pyinotify.WatchManager()
jobQueue = Queue.Queue()

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
    def __init__(self, path):
        self.path = path
        self.size = os.path.getsize(path)
    def changed(self):
        return self.size != os.path.getsize(self.path)

class JobRunner(threading.Thread):
    vmProcess = None
    currentJob = None
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = JobLogger(None)

    def switchJob(self):
        jobName = "None"
        if self.currentJob:
            jobName = str(self.currentJob.path)
        self.logger.debug("Switching to " + jobName)
        self.logger = JobLogger(jobName)

    def waitForEndOfRunningJob(self):
        if self.vmProcess != None:
            self.logger.info("Waiting for job to finish")
            timeout = time.time() + 60*5
            while self.vmProcess.returncode == None and time.time() < timeout:
                #TODO Use vmProcess.wait(timeout=20) when 3.3 has hit the servers
                self.vmProcess.poll()
                time.sleep(20)
            if self.vmProcess.returncode == None:
                self.logger.warn("Killing job")
                self.vmProcess.kill()
            self.logger.info("End")
            self.vmProcess = None

    def startJob(self):
        self.logger.info("Start")
        os.rename(self.currentJob.path, "job.img")
        assert os.path.exists("job.img")
        assert os.path.exists("debian.raw")
        self.vmProcess = subprocess.Popen(args = [
            "/usr/bin/kvm",
            "-net", "none",
            "-no-fd-bootchk",
            "-nographic",
            "-enable-kvm",
            "-no-reboot",
            "-drive",
            "-m", "1G",
            "file=debian.raw,index=0,media=disk,snapshot=on",
            "-drive",
            "file=job.img,index=1,media=disk"],
            stdin=None, stdout=file("/dev/null", 'w'), stderr=subprocess.STDOUT,
            close_fds=True)
        self.logger.info("Started with pid %i" % self.vmProcess.pid)

    def saveJobImage(self):
        assert self.currentJob
        outputName = os.path.basename(self.currentJob.path) + "_" + datetime.datetime.now().isoformat()
        self.logger.info("Saving output to: " + outputName)
        os.rename(
            "job.img",
            os.path.join("done", outputName)
            )
        assert not os.path.exists("job.img")

    def moveJobToDone(self):
        assert self.vmProcess == None
        self.logger.info("Moving job to done")
        if os.path.exists("job.img"):
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

    def process_IN_CLOSE_WRITE(self, event):
        if event.name:
            self.verifyAndQueue(os.path.join(event.path, event.name))
    def process_IN_CLOSE_NOWRITE(self, event):
        if event.name:
            self.verifyAndQueue(os.path.join(event.path, event.name))
    def process_IN_MOVED_TO(self, event):
        if event.name:
            self.verifyAndQueue(os.path.join(event.path, event.name))

    def verifyAndQueue(self, jobPath):
        logging.info("Adding job to queue: %s", jobPath)
        jobQueue.put(Job(jobPath))

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    if not os.path.exists("done"):
        os.mkdir("done")
    if not os.path.exists("queue"):
        os.mkdir("queue")
    jr = JobRunner()
    jr.start()
    notifier = pyinotify.Notifier(wm, QueueEventHandler())
    wdd = wm.add_watch('queue', QueueEventHandler.mask , rec=False)
    notifier.loop()
    jobQueue.put(None)
    logging.info("Joining with jobrunner")
    if jr.isAlive():
        jr.join()




