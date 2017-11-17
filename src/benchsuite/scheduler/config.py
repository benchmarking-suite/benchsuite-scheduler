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
        self.docker_results_storage_secret = 'storage'
        self.docker_host = 'localhost:2375'
        self.docker_benchsuite_image = 'benchsuite/benchsuite-multiexec:dev'
        self.docker_containers_env = {
            'proxy': 'test_val'
        }
        self.docker_containers_tags = ['global']
        self.docker_containers_additional_opts = ['--tag', 'gloabl_tag']
        self.schedules_sync_interval = 60  # seconds
        self.print_jobs_info_interval = 60  # seconds




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

