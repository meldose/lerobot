# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform
import time
from lerobot.robots import Robot # imported Robot class
# created function for busy_wait

def busy_wait(seconds):
    if platform.system() == "Darwin" or platform.system() == "Windows" or platform.system()=="Linux":
        # On Mac and Windows, `time.sleep` is not accurate and we need to use this while loop trick,
        # but it consumes CPU cycles.
        end_time = time.perf_counter() + seconds
        while time.perf_counter() < end_time:
            pass
    else:
        # On Linux time.sleep is accurate
        if seconds > 0:
            time.sleep(seconds)


robot=Robot() # crearted Robot object

# created function for safe_disconnect
def safe_disconnect(func):
    # TODO(aliberts): Allow to pass custom exceptions
    # (e.g. ThreadServiceExit, KeyboardInterrupt, SystemExit, UnpluggedError, DynamixelCommError)
    def wrapper(robot, *args, **kwargs):
        try:
            return func(robot, *args, **kwargs)
        except Exception as e:
            if robot.is_connected:
                robot.disconnect()
            raise e

    return wrapper

# calling all the functions
busy_wait(seconds=1.0)
wrapper=safe_disconnect(func=robot.disconnect)
wrapper(robot)