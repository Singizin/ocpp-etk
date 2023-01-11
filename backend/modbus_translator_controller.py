import asyncio
import time
import socket

from backend.modbus_translator import Modbus
from backend.tcp_server import Server, ReceiveEvebtCallBack

HOST = '127.0.0.1'
PORT = 8001  # https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers


async def start_changing_modbus(modbus: Modbus):
    hname = socket.gethostname()
    print(hname)
    ip = socket.gethostbyname(hname) or HOST
    server = Server(host=ip, port=PORT)

    def change_voltage_a(*, message, **kwargs):
        modbus.voltage_a = message

    server.SetReceiveEventCallBack(change_voltage_a)
    server.Start()

    while True:
        await asyncio.sleep(1)
