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

from benchsuite.scheduler.synchronizer import sync_jobs

logger = logging.getLogger(__name__)

def synch_scheduled_jobs(bsscheduler):
    """
    This function is scheduled as jobs and periodically
    syncrhonize the jobs in the scheduler with the schedules db
    """

    schedules = bsscheduler.schedules_db.get_benchmarking_schedules()

    print('Found {0} schedules'.format(len(schedules)))

    sync_jobs(schedules, bsscheduler.scheduler)

    return 123

