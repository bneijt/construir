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

NULL = file(os.path.devnull, 'w')

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
            timeout = time.time() + 60*5
            while self.vmProcess.returncode == None and time.time() < timeout:
                #TODO Use vmProcess.wait(timeout=20) when 3.3 has hits the debian servers
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
            "-m", "1G",
            "-drive",
            "file=debian.raw,index=0,media=disk,snapshot=on",
            "-drive",
            "file=job.img,index=1,media=disk"],
            stdin=None, stdout=NULL, stderr=subprocess.STDOUT,
            close_fds=True)
        self.logger.info("Started with pid %i" % self.vmProcess.pid)

    def saveJobImage(self):
        assert self.currentJob
        outputName =  datetime.datetime.now().strftime("%Y-%m-%sT%H_%M_%S") + "_" + os.path.basename(self.currentJob.path) + ".bz2"
        self.logger.info("Saving output to: " + outputName)
        outputPath = os.path.join(self.config.done, outputName)
        bz = subprocess.Popen(["bzip2", "-c", "job.img"],
            stdin=None, stdout=file(outputPath, "w"), stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = bz.communicate()
        bz.wait()
        if len(stderrdata):
            logger.error("bzip2 reported errors '%s'" % stderrdata)
        os.unlink("job.img")
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
    parser = argparse.ArgumentParser(description='Run construir jobs entered into the queue directory')
    parser.add_argument("--queue", help = "Directory to queue", default = "./queue")
    parser.add_argument("--done", help = "Directory to store finalized jobs", default = "./done")

    config = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    if not os.path.exists(config.done):
        os.mkdir(config.done)
    if not os.path.exists(config.queue):
        os.mkdir(config.queue)
    if not os.path.exists("debian.raw"):
        logging.error("Could not find guest image ./debian.raw")
        return 1

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

