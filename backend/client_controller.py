import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.client import ChargePoint


async def start_listening_server(cp: 'ChargePoint'):
    print(cp._connection)
    while True:
        if cp._connection:
            # cmd = input('client command: ')  # async input()
            # if cmd == 'b':
            #     await cp.send_boot_notification()
            # if cmd == 's':
            #     await cp.send_status_notification()
            # if cmd == 'print':
            #     cp.modbus.print_state()
            await asyncio.sleep(1)
