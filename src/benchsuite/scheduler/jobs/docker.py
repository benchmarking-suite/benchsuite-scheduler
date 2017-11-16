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
from typing import Any, List

import docker
import time
from docker.types import SecretReference, RestartPolicy

from benchsuite.scheduler.bsscheduler import get_bsscheduler

logger = logging.getLogger(__name__)


def __get_secret_ref(client, name_or_id):

    for s in client.secrets.list():
        if s.id == name_or_id or s.name == name_or_id:
            return SecretReference(s.id, s.name)

    return None


class DockerJobFailedException(Exception):

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.retval = None
        self.log = None


def __wait_for_execution(client, service):

    retry = 5
    cont_id = None
    while retry and not cont_id:
        service.reload()
        if len(service.tasks()) > 0:
            task = service.tasks()[0]
            if 'ContainerID' in task['Status']['ContainerStatus']:
                cont_id = task['Status']['ContainerStatus']['ContainerID']
                break

        retry -= 1
        logger.debug('Container ID not ready yet. Retrying in 2 seconds')
        time.sleep(2)

    if not cont_id:
        raise Exception('Failed to retrieve the container id after 10 seconds')

    task = service.tasks()[0]


    cont_id = task['Status']['ContainerStatus']['ContainerID']
    cont = client.containers.get(cont_id)
    retval = cont.wait()
    log = cont.logs().decode()

    return retval, log


def docker_job(
        username: str,
        provider_config_secret: str,
        tests: List[str],
        tags = [],
        env = {},
        additional_opts = []):

    logger.debug('Starting Docker job')

    config = get_bsscheduler().config

    client = docker.DockerClient(config.docker_host)

    storage_secret = __get_secret_ref(client, config.results_storage_secret)
    provider_secret = __get_secret_ref(client, provider_config_secret)
    restartCond = RestartPolicy(condition='none')

    args = [
        '--storage-config', '/run/secrets/' + storage_secret['SecretName'],
        '--provider', '/run/secrets/' + provider_secret['SecretName'],
        '--failonerror',
        '--user', username
    ]

    for t in tags:
        args.extend(['--tag', t])

    # are we sure we want always to append the additional options?
    args.extend(config.docker_containers_additional_opts)
    args.extend(additional_opts)

    args.extend(tests)

    final_env = dict(config.docker_containers_env)
    final_env.update(env)
    env_list = ['{0}={1}'.format(k,v) for k,v in final_env.items()]

    service = client.services.create(
        config.docker_benchsuite_image,
        secrets=[storage_secret, provider_secret],
        args=args,
        env=env_list,
        restart_policy = restartCond
    )

    retval, log = __wait_for_execution(client, service)

    service.remove()

    if retval != 0:
        e = DockerJobFailedException(
            'The execution exit with status {0}'.format(retval))
        e.log = log
        raise e

    return retval

