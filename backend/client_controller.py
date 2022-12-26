import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.client import ChargePoint


async def start_listening_server(cp: 'ChargePoint'):
    print(cp._connection)
    while True:
        if cp._connection:
            cmd = input()
            if cmd == 'b':
                await cp.send_boot_notification()
            await asyncio.sleep(1)
