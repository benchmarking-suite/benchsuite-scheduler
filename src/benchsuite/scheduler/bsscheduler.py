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

from apscheduler.events import EVENT_SCHEDULER_SHUTDOWN, EVENT_ALL
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from benchsuite.scheduler.jobs.meta import synch_scheduled_jobs
from benchsuite.scheduler.logger import JobExecutionLogger
from benchsuite.scheduler.schedules import BenchmarkingSchedulesDB

logger = logging.getLogger(__name__)



# we want to have a global instance of BSScheduler so that jobs can access it
# we do not want to specify the BSScheduler instance as jobs parameters because
# in this case it would be serialized in the jobs status while we want a fresh
# instance if we restart the scheduler
__instance = None


def get_bsscheduler():
    """
    Returns the global instance of the BSScheduler
    :return:
    """
    return __instance


def create_bsscheduler():
    """
    Creates a new global instance of the BSSCheduler
    :return:
    """
    global __instance
    __instance = BSScheduler()
    return get_bsscheduler()





class BenchsuiteSchedulerConfig(object):

    def __init__(self, config_dict):

        self.jobs_db_host = config_dict['connection_string']
        self.jobs_db_name = config_dict['db_name']
        self.jobs_collection = config_dict['collection']
        self.schedules_db_host = config_dict['connection_string']
        self.schedules_db_name = config_dict['qoe_db_name']
        self.schedules_collection = config_dict['qoe_schedules_collection']
        self.jobs_execution_logger_db_host = config_dict['connection_string']
        self.jobs_execution_logger_db_name = config_dict['log_db_name']
        self.jobs_execution_logger_collection = config_dict['log_collection']
        self.results_storage_secret = 'storage'
        self.docker_host = 'localhost:2375'
        self.docker_benchsuite_image = 'benchsuite/benchsuite-multiexec:dev'
        self.docker_containers_env = {
            'proxy': 'test_val'
        }
        self.docker_containers_additional_opts = ['--tag', 'gloabl_tag']




def load_configuration():
    return BenchsuiteSchedulerConfig({
        'connection_string': 'mongodb://localhost:27017/',
        'db_name': 'benchmarking',
        'collection': 'ap_jobs',
        'qoe_db_name': 'benchmarking',
        'qoe_schedules_collection': 'scheduling',
        'log_db_name': 'benchmarking',
        'log_collection': 'ap_executions'
    })

class BSScheduler(object):
    """
    This class wraps the information that might be needed to the Jobs
    """

    config = None
    scheduler = None
    schedulesdb = None
    jobslogger = None

    __initialized = False

    def __init__(self):
        self.config = load_configuration()
        self.__blocked_flag = None

    def initialize(self):
        """
        Initialize the scheduler
        :return:
        """

        # load the schedules configuration
        self.schedules_db = BenchmarkingSchedulesDB(
            self.config.schedules_db_host,
            self.config.schedules_db_name,
            self.config.schedules_collection)

        # initialize the APScheduler
        jobstore = MongoDBJobStore(
            database=self.config.jobs_db_name,
            collection=self.config.jobs_collection,
            host=self.config.jobs_db_host
        )

        self.scheduler = BackgroundScheduler(jobstores={
            'benchmarking_jobs':jobstore,
            'meta_jobs': MemoryJobStore()})

        logger.debug('New APScheduler created: ' + str(self.scheduler))

        # if we do not start the scheduler, the jobstores are not initialized
        # and the old jobs (from the DB) are not visible (they are needed
        # because we want to sync the store before starting to execute the jobs)
        self.scheduler.start(paused=True)

        self.__add_meta_jobs()

        # initialize the job logger facility
        self.jobslogger = JobExecutionLogger(
            self.config.jobs_execution_logger_db_host,
            self.config.jobs_execution_logger_db_name,
            self.config.jobs_execution_logger_collection
        )
        self.scheduler.add_listener(
            self.jobslogger.apscheduler_listener, EVENT_ALL)

        self.__initialized = True

    def __add_meta_jobs(self):
        logger.debug('Adding meta job to sync schedules')
        self.scheduler.add_job(synch_scheduled_jobs, 'interval', seconds=5,
                               id='_sync_schedules', replace_existing=True,
                               max_instances=1,
                               args=[self],
                               jobstore='meta_jobs')

    def start(self):
        """
        Starts to process jobs. This method also initializes the scheduler is
        not done
        :return:
        """
        if not self.__initialized:
            logger.warning('The scheduler is not initialized. Initializing it'
                           'before starting')
            self.initialize()

        logger.info('String processing the jobs')
        self.scheduler.resume()

    def shutdown(self):
        """
        Stops the scheduler
        :return:
        """
        logger.info('Shutting down the scheduler')
        self.scheduler.shutdown()

    def wait_unitl_shutdown(self):
        """
        Blocking call to wait until the scheduler is shutoff
        :return:
        """
        self.scheduler.add_listener(self.__scheduler_listener,
                                    EVENT_SCHEDULER_SHUTDOWN)

        self.__blocked_flag = threading.Condition()

        with self.__blocked_flag:
            self.__blocked_flag.wait()

    def __scheduler_listener(self, event):
        if event.code == EVENT_SCHEDULER_SHUTDOWN:
            with self.__blocked_flag:
                self.__blocked_flag.notify()








