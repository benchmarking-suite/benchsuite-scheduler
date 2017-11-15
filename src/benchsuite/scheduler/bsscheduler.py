# Benchmarking Suite
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)
import logging
import threading
from random import random

from apscheduler.events import EVENT_SCHEDULER_SHUTDOWN
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from benchsuite.scheduler.config import load_configuration
from benchsuite.scheduler.job.internal import print_scheduled_jobs, \
    synch_scheduled_jobs
from benchsuite.scheduler.schedulesconfig import BenchmarkingScheduleConfigDB

logger = logging.getLogger(__name__)




class BSScheduler(object):
    """
    This class wraps the information that might be needed to the Jobs
    """

    config = None
    scheduler = None
    schedulesdb = None

    def __init__(self):
        self.config = load_configuration()

    def initialize(self):

        # initialize the connection with the schedules database
        self.schedules_db = BenchmarkingScheduleConfigDB(self.config)

        # initialize the jobstore and the scheduler
        jobstore = MongoDBJobStore(
            database=self.config.jobs_db_name,
            collection=self.config.jobs_collection,
            host=self.config.jobs_db_host
        )
        self.scheduler = BackgroundScheduler(jobstores={
            'benchmarking_jobs':jobstore,
            'meta_jobs': MemoryJobStore()})

        logger.debug('New APScheduler created: ' + str(self.scheduler))

        # if we do not start the scheduler, the sotres are not initialized
        # and the old jobs (from the DB) are not visible (they are needed
        # because we want to sync the store before starting to execute the jobs)
        self.scheduler.start(paused=True)

        self.__add_meta_jobs()



    def __add_meta_jobs(self):
        logger.debug('Adding meta jobs')

        self.scheduler.add_job\
            (print_scheduled_jobs, 'interval', seconds=30,
             id='_print_jobs', replace_existing=True, max_instances=1,
             jobstore='meta_jobs')

        self.scheduler.add_job(synch_scheduled_jobs, 'interval', seconds=5,
                               id='_print_jobs', replace_existing=True,
                               max_instances=1,
                               jobstore='meta_jobs')



    def start(self):
        #TODO check that the init step has been done

        logger.info('String processing the jobs')
        self.scheduler.resume()

    def wai_unitl_shutdown(self):
        self.scheduler.add_listener(self.__scheduler_listener,
                                    EVENT_SCHEDULER_SHUTDOWN)

        self.__blocked_flag = threading.Condition()

        with self.__blocked_flag:
            self.__blocked_flag.wait()


    def __scheduler_listener(self, event):
        if event.code == EVENT_SCHEDULER_SHUTDOWN:
            with self.__blocked_flag:
                self.__blocked_flag.notify()


    def shutdown(self):
        logger.info('Shutting down the scheduler')
        self.scheduler.shutdown()





# we want to have a global instance of BSScheduler so that jobs can access it
# we do not want to specify the BSScheduler instance as job parameters because
# in this case it would be serialized in the job status while we want a fresh
# instance if we restart the scheduler
__instance = None


def get_bsscheduler() -> BSScheduler:
    """
    Returns the global instance of the BSScheduler
    :return:
    """
    return __instance


def create_bsscheduler() -> BSScheduler:
    """
    Creates a new global instance of the BSSCheduler
    :return:
    """
    global __instance
    __instance = BSScheduler()
    return get_bsscheduler()
