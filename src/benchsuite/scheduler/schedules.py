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

from pymongo import MongoClient

logger = logging.getLogger(__name__)

_DEFAULT_INTERVAL = {
    'weeks': 0,
    'days': 0,
    'hours': 0,
    'minutes': 0,
    'seconds': 0
    }

class BenchmarkingScheduleConfig(object):

    interval = None
    cloud_config = None
    storage_config = None

    def __init__(self, raw_obj):
        self._raw_obj = raw_obj

        self.id = raw_obj['id']

        if 'interval' in raw_obj:
            raw_interval = raw_obj['interval']
            try:
                self.interval = {
                    k:int(raw_interval[k]) if k in raw_interval else v
                    for k, v in _DEFAULT_INTERVAL.items()}
            except ValueError:
                logger.error('Error parsing schedule interval. All interval '
                             'values must be integer')
                raise

        if 'cloud_config' in raw_obj:
            self.cloud_config = raw_obj['cloud_config']

        if 'storage_config' in raw_obj:
            self.storage_config = raw_obj['storage_config']



class BenchmarkingSchedulesDB(object):


    def __init__(self, db_host, db_name, collection):
        self._client = MongoClient(db_host)
        self._db_name = db_name
        self._collection = collection

    def get_benchmarking_schedules(self):
        out = []
        for r in self._client[self._db_name][self._collection].find():
            try:
                out.append(BenchmarkingScheduleConfig(r))
            except:
                logger.error('Schedule %s malformed. Not considering it',
                             r['id'])

        return out
