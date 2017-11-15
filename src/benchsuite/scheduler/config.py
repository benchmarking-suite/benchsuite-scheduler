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



# TODO remove static configuration
def load_configuration():
    return BenchsuiteSchedulerConfig({
        'connection_string': 'mongodb://localhost:27017/',
        'db_name': 'benchmarking',
        'collection': 'ap_jobs',
        'qoe_db_name': 'benchmarking',
        'qoe_schedules_collection': 'scheduling'
    })


class BenchsuiteSchedulerConfig(object):

    def __init__(self, config_dict):

        self.jobs_db_host = config_dict['connection_string']
        self.jobs_db_name = config_dict['db_name']
        self.jobs_collection = config_dict['collection']
        self.schedules_db_host = config_dict['connection_string']
        self.schedules_db_name = config_dict['qoe_db_name']
        self.schedules_collection = config_dict['qoe_schedules_collection']


