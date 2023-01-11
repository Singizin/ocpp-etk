import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.server import ChargePoint


async def start_listening_server(cp: 'ChargePoint'):
    print(cp._connection)
    # while True:
    if cp._connection:
        cmd = input('server command: ')
        if cmd == 'ca':
            print('got', await cp.send_change_availability())
        await asyncio.sleep(1)
