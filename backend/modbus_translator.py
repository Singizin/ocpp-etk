import asyncio
import dataclasses
import random
import time
from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict, List, TYPE_CHECKING, Union

import ocpp.v16.enums as enums

if TYPE_CHECKING:
    from backend.client import ChargePoint


class MeterValues:
    def __init__(self):
        self._power_active_import = 40
        self._soc = 87
        self._current_import = 23
        self._voltage = 220

    @property
    def get_values(self):
        return [{'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z",
                 'sampledValue': [{'value': str(x)} for x in [*self.__dict__.values()]]}]

    @property
    def power_active_import(self):
        return self._power_active_import


class Modbus:
    _hooks: Dict[str, List[Callable]]

    def set_cp(self, cp):
        self.cp = cp

    def trigger_callbacks(self, field_name: str):
        for callable_ in self._hooks.get(field_name, []):
            callable_()

    def register_hook(self, field_name: str, callback: Callable):
        print(f'register hook for {field_name=}')
        self._hooks[field_name].append(callback)

    async def wait_for_change(self, field_name: str):
        old_value = getattr(self, field_name)
        while True:
            new_value = getattr(self, field_name)
            print(field_name, new_value, old_value)
            if new_value != old_value:
                return new_value
            await asyncio.sleep(0.1)

    def __init__(self):
        self._hooks = defaultdict(list)
        self.cp: Union['ChargePoint', None] = None
        self.meter_values = MeterValues()
        self.connector_id = 1
        # self.type = None
        self._charge_point_error_code: Union[enums.ChargePointErrorCode, None] = enums.ChargePointErrorCode.no_error
        self._availability_type: Union[enums.AvailabilityType, None] = None
        self._availability_status: Union[enums.AvailabilityStatus, None] = None
        self._charge_point_status: Union[enums.ChargePointStatus, None] = None

    def print_state(self):
        print(self.__dict__)

    #region charge_point_status
    @property
    def charge_point_status(self):
        return self._charge_point_status

    @charge_point_status.setter
    def charge_point_status(self, value):
        self._charge_point_status = value
        self.trigger_callbacks('charge_point_status')
    #endregion

    # region availability_status
    @property
    def availability_status(self):
        return self._availability_status

    @availability_status.setter
    def availability_status(self, value):
        self._availability_status = value
        self.trigger_callbacks('availability_status')
    #endregion

    # region availability_type
    @property
    def availability_type(self):
        return self._availability_type

    @availability_type.setter
    def availability_type(self, value):
        self._availability_type = value

    # endregion

    async def set_availability_status(self, type):
        # request
        await asyncio.sleep(2)

        self.availability_type = type
        self.availability_status = random.choice([
            enums.AvailabilityStatus.accepted,
            enums.AvailabilityStatus.rejected,
            enums.AvailabilityStatus.scheduled,
        ])
        await asyncio.sleep(1)
        # setattr(self, 'status_2', type)

    # region charge_point_error_code
    @property
    def charge_point_error_code(self):
        return self._charge_point_error_code

    @charge_point_error_code.setter
    def charge_point_error_code(self, value):
        self._charge_point_error_code = value
    #endregion


