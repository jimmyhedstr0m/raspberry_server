import sys
import smbus
from response_interface import Response


class Temperature(Response):

    def __init__(self):
        pass

    def get_temperature(self, address=0x48):
        try:
            bus = smbus.SMBus(1)
            raw = bus.read_word_data(address, 0) & 0xFFFF
            raw = ((raw << 8) & 0xFF00) + (raw >> 8)
            temperature = (raw / 32.0) / 8.0
            temperature = "{0:0.2f}".format(temperature)

            results = {
                "room_temperature": temperature,
                "unit": "celsius"
            }

            return Response.succ_response(self, results)
        except:
            return Response.err_response(self, "Unexpected error:", sys.exc_info()[0])
