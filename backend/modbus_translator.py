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
        self.power_active_import = 40
        self.soc = 87
        self.current_import = 23
        self.voltage = 220

    @property
    def get_values(self):
        return [{'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z",
                'sampledValue': [{'value': str(x)} for x in [*self.__dict__.values()]]}]


class Modbus:
    _hooks: Dict[str, List[Callable]]

    def __init__(self):
        self._hooks = defaultdict(list)
        self.cp: Union['ChargePoint', None] = None
        self.meter_values = MeterValues()
        self.error = 0
        self.connector_id = None
        self.type = None
        self._availability_status: Union[enums.AvailabilityStatus, None] = None
        self._charge_point_status: Union[enums.ChargePointStatus, None] = None

    def set_cp(self, cp):
        self.cp = cp

    @property
    def voltage_a(self):
        return self._voltage_a

    @voltage_a.setter
    def voltage_a(self, value):
        print(f'changed voltage_a {value}')
        self._voltage_a = value

    @property
    def charge_point_status(self):
        return self._charge_point_status

    @charge_point_status.setter
    def charge_point_status(self, value):
        self._charge_point_status = value
        asyncio.create_task(self.cp.send_status_notification(value))

    @charge_point_status.getter
    def charge_point_status(self):
        return self._charge_point_status

    def getter_availability_status(self):
        if self.error == 1:
            return enums.AvailabilityStatus.rejected
        if self.error == 0:
            return enums.AvailabilityStatus.accepted

    def register_hook(self, field_name: str, callback: Callable):
        self._hooks[field_name].append(callback)

    async def wait_for_change(self, field_name: str, background: bool = False):
        old_value = getattr(self, field_name)
        if not background:
            while True:
                new_value = getattr(self, field_name)
                print(field_name, new_value, old_value)
                if new_value != old_value:
                    return new_value
                await asyncio.sleep(0.1)

    def trigger_callbacks(self, field_name: str):
        for callable_ in self._hooks.get(field_name, []):
            callable_()

    async def set_availability_status(self):
        # request
        await asyncio.sleep(2)
        self.charge_point_status = random.choice([
            enums.AvailabilityStatus.accepted,
            enums.AvailabilityStatus.rejected,
            enums.AvailabilityStatus.scheduled,
        ])
        await asyncio.sleep(1)
        # setattr(self, 'status_2', type)

    def print_state(self):
        print(self.__dict__)
