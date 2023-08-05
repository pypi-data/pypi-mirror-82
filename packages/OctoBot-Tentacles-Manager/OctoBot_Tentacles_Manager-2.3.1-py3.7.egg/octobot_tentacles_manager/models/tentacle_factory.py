#  Drakkar-Software OctoBot-Tentacles-Manager
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import octobot_tentacles_manager.models as models


class TentacleFactory:
    def __init__(self, tentacle_root_path):
        self.tentacle_root_path = tentacle_root_path

    def create_tentacle_from_type(self, name, tentacle_type):
        return models.Tentacle(self.tentacle_root_path, name, tentacle_type)

    async def create_and_load_tentacle_from_module(self, tentacle_module):
        tentacle_type = models.TentacleType.from_import_path(self.tentacle_root_path, tentacle_module.__name__)
        tentacle = models.Tentacle(self.tentacle_root_path, tentacle_type.module_name, tentacle_type)
        await tentacle.initialize()
        return tentacle
