from response_interface import Response


class Temperature(Response):

    def get_temperature(self, address=0x48):
        try:
            import sys
            import smbus

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
        except ImportError:
            err_string = "Python libraries needed for temperature"
            err_string += " measurement not installed"
            return Response.err_response(self, err_string)
