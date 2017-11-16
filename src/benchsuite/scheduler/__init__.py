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
from benchsuite.scheduler.bsscheduler import BSScheduler

VERSION = (1, 0, 0, '0')
# we want to have a global instance of BSScheduler so that jobs can access it
# we do not want to specify the BSScheduler instance as jobs parameters because
# in this case it would be serialized in the jobs status while we want a fresh
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

