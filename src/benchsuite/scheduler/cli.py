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
import signal
import time
import sys

from benchsuite.scheduler.bsscheduler import get_bsscheduler, create_bsscheduler

logger = logging.getLogger(__name__)

def on_exit(sig, func=None):
    get_bsscheduler().shutdown()
    print('Bye bye...')
    sys.exit(1)


def main(args=None):

    signal.signal(signal.SIGINT, on_exit)

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout)

    logging.getLogger('apscheduler').setLevel(logging.WARN)

    logger.info('Logging configured')

    bsscheduler = create_bsscheduler()
    bsscheduler.initialize()
    bsscheduler.start()

    # wait for the APScheduler thread finishes. This will happen when the
    # scheduler is shut down from a SIGINT (see on_exit function)
    #bsscheduler.scheduler._thread.join()

    bsscheduler.wait_unitl_shutdown()



if __name__ == '__main__':
    main(sys.argv[1:])