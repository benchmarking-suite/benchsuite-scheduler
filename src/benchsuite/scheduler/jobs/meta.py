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

import docker
import pytz
from tzlocal import get_localzone

from benchsuite.scheduler.synchronizer import sync_jobs

logger = logging.getLogger(__name__)

def sync_scheduled_jobs(bsscheduler):
    """
    This function is scheduled as jobs and periodically
    syncrhonize the jobs in the scheduler with the schedules db
    """

    schedules = bsscheduler.schedules_db.get_benchmarking_schedules()

    sync_jobs(schedules, bsscheduler.scheduler)

    return 0


def print_scheduled_jobs_info(bsscheduler):
    """
    print some information on the status of the scheduler
    :param bsscheduler:
    :return:
    """
    out = []
    jobs = bsscheduler.scheduler.get_jobs(jobstore='benchmarking_jobs')

    out.append('********************************************************')
    out.append('*                    SCHEDULED JOBS                    *')
    out.append('*                                                      *')
    for j in jobs:
        out.append(u'* - {0} \u27A1 {1}'.format(j.args[0].id, str(j.next_run_time.strftime('%Y-%m-%d %H:%M:%S'))))
    out.append('*                                                      *')
    out.append('*                     RUNNING JOBS                     *')

    all_instances = bsscheduler.dockermanager.list()

    for i in [i for i in all_instances if i.status == 'running']:
        localdatetime = pytz.utc.localize(i.created).astimezone(get_localzone())
        out.append('* - {0} {1}'.format(i.schedule_id, localdatetime.strftime('%Y-%m-%d %H:%M:%S')))
    out.append('*                                                      *')
    out.append('*                  NOT RUNNING INSTANCE                *')
    for i in [i for i in all_instances if i.status != 'running']:
        localdatetime = pytz.utc.localize(i.created).astimezone(get_localzone())
        out.append('* - {0} {1}'.format(i.schedule_id, localdatetime.strftime('%Y-%m-%d %H:%M:%S')))
    out.append('*                                                      *')
    out.append('********************************************************')

    print('\n'.join(out))
