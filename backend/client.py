import asyncio
import logging
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

    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        # if response.status == "Accepted":
        #     print("Connected to central system.")
        #     await self.send_heartbeat(response.interval)

    async def send_status_notification(self, a):
        """Send a status notification."""
        request = call.StatusNotificationPayload(
            connector_id=0,
            error_code=enums.ChargePointErrorCode.no_error,
            status=enums.ChargePointStatus.available,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            info=f'Test info {a=}',
            vendor_id="The Mobility House",
            vendor_error_code="Test error",
        )
        resp = await self.call(request)

    @on(Action.ChangeAvailability)
    async def on_change_availability(self, connector_id, type):
        wait_task = asyncio.create_task(self.modbus.wait_for_change('status'))
        asyncio.create_task(self.modbus.set_availability_status(connector_id, type))
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

        await asyncio.gather(
            cp.start(),
            cp.send_boot_notification(),
            start_listening_server(cp),
            start_changing_modbus(modbus)
            # (modbus),
        )


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
