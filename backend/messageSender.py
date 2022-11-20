import asyncio
import logging

from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)

