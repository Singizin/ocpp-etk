import asyncio
import logging
import time
from datetime import datetime, timezone

from backend.client_controller import start_listening_server
from backend.modbus_translator import Modbus
from backend.modbus_translator_controller import start_changing_modbus

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
import ocpp.v16.enums as enums
from ocpp.v16.enums import Action

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    def __init__(self, *args, **kwargs):
        modbus = kwargs.pop('modbus')

        super().__init__(*args, **kwargs)

        self.modbus = modbus
        modbus.set_cp(self)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        if response.status == "Accepted":
            print("Connected to central system.")
            await self.send_heartbeat(response.interval)

    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    async def send_status_notification(self):
        """Send a status notification."""
        request = call.StatusNotificationPayload(
            connector_id=0,
            error_code=enums.ChargePointErrorCode.no_error,
            status=self.modbus.charge_point_status,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            info='Test info',
            vendor_id="The Mobility House",
            vendor_error_code="Test error",
        )
        resp = await self.call(request)

    async def send_meter_values(self,
                                connector_id: int = 0):
        request = call.MeterValuesPayload(
            connector_id=connector_id,
            transaction_id=0,
            meter_value=self.modbus.meter_values.get_values
        )
        r = await self.call(request)

    async def send_start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=0,
            meter_start=self.modbus.meter_values.get_values['power_active_export'],
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )
        r = await self.call(request)

    @on(Action.ChangeAvailability)
    async def on_change_availability(self,
                                     connector_id,
                                     type):
        wait_task = asyncio.create_task(self.modbus.wait_for_change('availability_status'))
        asyncio.create_task(self.modbus.set_availability_status())
        status = await wait_task
        return call_result.ChangeAvailabilityPayload(
            status=status,  # enums.AvailabilityStatus.accepted
        )


async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_123',
            subprotocols=['ocpp1.6']
    ) as ws:
        modbus = Modbus()
        cp = ChargePoint('CP_123', ws, modbus=modbus)

        modbus.register_hook('charge_point_status', lambda:  asyncio.create_task(cp.send_status_notification()))

        await asyncio.gather(
            cp.start(),
            cp.send_boot_notification(),
            cp.send_meter_values(),
            # start_listening_server(cp),
            start_changing_modbus(modbus)
            # (modbus),
        )


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
