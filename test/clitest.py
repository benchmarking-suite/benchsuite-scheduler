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
import sys

import os

from benchsuite.scheduler.cli import main

if __name__ == '__main__':

    os.environ['DB_HOST'] = 'mongodb://localhost:27017'
    #os.environ['DOCKER_HOST'] = 'tcp://localhost:4550'
    os.environ['DOCKER_HOST'] = 'unix://var/run/docker.sock'
    os.environ['DOCKER_STORAGE_SECRET'] = 'storage'
    os.environ['DOCKER_ADDITIONAL_OPTS'] = 'hosts={"cloudpctn":"10.0.1.1"}'
    os.environ['BENCHSUITE_GLOBAL_TAGS'] = 'pippo'
    main([])

