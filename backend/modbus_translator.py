import asyncio
import random
import time
from collections import defaultdict
from typing import Callable, Dict, List, TYPE_CHECKING, Union

import ocpp.v16.enums as enums

if TYPE_CHECKING:
    from backend.client import ChargePoint


class Modbus:
    _hooks: Dict[str, List[Callable]]

    def __init__(self):
        self._hooks = defaultdict(list)
        self.cp: Union['ChargePoint', None] = None

        self.error = 0
        self._voltage_a = 0
        self.connector_id = None
        self.type = None
        self.status = None
        self._status_2 = None

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
    def status_2(self):
        return self._status_2

    @status_2.setter
    def status_2(self, value):
        self._status_2 = value
        asyncio.create_task(self.cp.send_status_notification(value))

    def getter_availability_status(self):
        if self.error == 1:
            return enums.AvailabilityStatus.rejected
        if self.error == 0:
            return enums.AvailabilityStatus.accepted

    def register_hook(self, field_name: str, callback: Callable):
        self._hooks[field_name].append(callback)

    async def wait_for_change(self, field_name: str):
        old_value = getattr(self, field_name)
        while True:
            new_value = getattr(self, field_name)
            print(field_name, new_value, old_value)
            if new_value != old_value:
                return new_value
            await asyncio.sleep(0.1)

    def trigger_callbacks(self, field_name: str):
        for callable_ in self._hooks.get(field_name, []):
            callable_()

    async def set_availability_status(self, connector_id, type):
        # request
        await asyncio.sleep(2)
        self.status = random.choice([
            enums.AvailabilityStatus.accepted,
            enums.AvailabilityStatus.rejected,
            enums.AvailabilityStatus.scheduled,
        ])
        await asyncio.sleep(2)
        setattr(self, 'status_2', type)

    def print_state(self):
        print(self.__dict__)
