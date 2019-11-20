# Copyright (c) 2018 SLIC personal studio.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from diveintoslic.job1.controllers import Users

class Routers(object):
    def add_routers(self, mapper):
        user_controller = Users()
        mapper.connect('/users/{user_name}',
                       controller=user_controller,
                       action='get_user',
                       conditions=dict(method=['GET']))

        mapper.connect('/users/{user_name}',
                       controller=user_controller,
                       action='delete_user',
                       conditions=dict(method=['DELETE']))

        mapper.connect('/users',
                       controller=user_controller,
                       action='create_user',
                       conditions=dict(method=['POST']))

        mapper.connect('/users/{user_name}',
                       controller=user_controller,
                       action='update_user',
                       conditions=dict(method=['PATCH']))

        mapper.connect('/users',
                       controller=user_controller,
                       action='list_users',
                       conditions=dict(method=['GET']))



