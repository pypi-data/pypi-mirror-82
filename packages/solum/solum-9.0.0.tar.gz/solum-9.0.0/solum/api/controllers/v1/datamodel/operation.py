# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from solum.api.controllers import common_types
from solum.api.controllers.v1.datamodel import types as api_types


class Operation(api_types.Base):
    """An Operation resource represents an operation or action.

    This is for defining actions that may change the state of the resource they
    are related to. For example, the API already provides ways to register,
    start, and stop your application (POST an Assembly to register+start, and
    DELETE an Assembly to stop) but Operations provide a way to extend the
    system to add your own actions such as "pause" and "resume", or "scale_up"
    and "scale_down".
    """

    documentation = common_types.Uri
    "Documentation URI for the operation."

    target_resource = common_types.Uri
    "Target resource URI to the operation."

    @classmethod
    def sample(cls):
        return cls(uri='http://example.com/v1/operations/resume',
                   name='resume',
                   type='operation',
                   tags=['small'],
                   project_id='1dae5a09ef2b4d8cbf3594b0eb4f6b94',
                   user_id='55f41cf46df74320b9486a35f5d28a11',
                   description='A resume operation',
                   documentation='http://example.com/docs/resume_op',
                   target_resource='http://example.com/instances/uuid')
