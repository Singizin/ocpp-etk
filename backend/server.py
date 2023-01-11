import asyncio
import logging
from datetime import datetime
import apiServer

import CMS_state
from backend.server_controller import start_listening_server

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
from ocpp.v16 import ChargePoint as cp
import ocpp.v16.enums as enums
from ocpp.v16.enums import Action
from ocpp.v16 import call_result, call

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=2,
            status=enums.RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        print("Got a Heartbeat!")
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )

    @on(Action.Authorize)
    def on_authorize(self, id_tag: str):
        return call_result.AuthorizePayload(
            id_tag_info=CMS_state.cmsIdTagInfo(idTag=id_tag)
        )

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, reservation_id: int,
                             timestamp: datetime):
        return call_result.StartTransactionPayload(
            id_tag_info=CMS_state.cmsIdTagInfo(idTag=id_tag),
            transaction_id=12345,
        )

    @on(Action.MeterValues)
    def on_meter_values(self, connector_id: int, transaction_id: int, meter_value: object):
        return call_result.MeterValuesPayload()

    @on(Action.StopTransaction)
    def on_stop_transaction(self, id_tag: str, meter_stop: int, timestamp: datetime,
                            transaction_id: int, reason: str, transaction_data: object, ):
        return call_result.StopTransactionPayload(id_tag_info=CMS_state.cmsIdTagInfo(id_tag))

    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id: int, error_code: str,
                               status: str, **kwargs):
        return call_result.StatusNotificationPayload()

    async def send_change_availability(self):
        request = call.ChangeAvailabilityPayload(
            connector_id=1,
            type=enums.AvailabilityType.inoperative
        )

        return await self.call(request)



async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.error(
            "Client hasn't requested any Subprotocol. Closing Connection"
        )
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    print(charge_point_id)
    cp = ChargePoint(charge_point_id, websocket)

    await asyncio.gather(cp.start(),
                         start_listening_server(cp))


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    # apiServer.run_server()

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
