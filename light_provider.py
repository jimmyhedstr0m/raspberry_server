from datetime import datetime
from response_interface import Response
from config_parser import ConfigParser
import json
import subprocess


class LightProvider(Response):

    def __init__(self):
        self.rooms = ConfigParser().get_rooms()
        self.init_room_states()

    def init_room_states(self):
        for room in self.rooms:
            room["power_on"] = False
            room["last_event"] = ""

            for key in room["units"]:
                unit = room["units"][key]

                unit["power_on"] = False
                unit["last_event"] = ""

    def _validate_room_id(self, room_id):
        return (room_id > -1 and room_id < len(self.rooms))

    def _error_validation(self, room_id, unit_id):
        if self._validate_room_id(room_id):
            if unit_id in self.rooms[room_id]["units"]:
                return False
            else:
                err_string = "Unable to find unit " + unit_id
                err_string += " in room " + str(room_id)
                return Response.err_response(self, err_string)
        else:
            err_string = "Unable to find room " + str(room_id)
            return Response.err_response(self, err_string)

    def _toggle(self, unit):
        if unit["type"] == "nexa":
            cmd = "pilight-send -p nexa_switch -i "
            keys = unit["unit_id"].split("-")
            remote_code = keys[0]
            unit_id = keys[1]

            cmd += remote_code + " -u " + unit_id + " -"
            if unit["power_on"]:
                cmd += "t"
            else:
                cmd += "f"

            print cmd
            subprocess.call(cmd, shell=True)
        elif unit["type"] == "lifx":
            print "Not implemented yet"

    def get_all_rooms(self):
        if len(self.rooms) > 0:
            return Response.succ_response(self, self.rooms)
        else:
            err_string = "Unable to find any rooms in config.json"
            return Response.err_response(self, err_string)

    def get_room(self, room_id):
        if self._validate_room_id(room_id):
            return Response.succ_response(self, self.rooms[room_id])
        else:
            err_string = "Unable to find room " + str(room_id)
            return Response.err_response(self, err_string)

    def get_room_unit(self, room_id, unit_id):
        error = self._error_validation(room_id, unit_id)
        if error:
            return error
        else:
            unit = self.rooms[room_id]["units"][unit_id]

            return Response.succ_response(self, unit)

    def toggle_room(self, room_id):
        if (self._validate_room_id(room_id)):
            room = self.rooms[room_id]
            room["power_on"] = not room["power_on"]
            room["last_event"] = str(datetime.now())

            for key in room["units"]:
                unit = room["units"][key]
                unit["power_on"] = room["power_on"]
                unit["last_event"] = str(datetime.now())
                self._toggle(unit)

            return Response.succ_response(self, self.rooms[room_id])
        else:
            err_string = "Unable to find room " + str(room_id)
            return Response.err_response(self, err_string)

    def toggle_unit(self, room_id, unit_id):
        error = self._error_validation(room_id, unit_id)
        if error:
            return error
        else:
            unit = self.rooms[room_id]["units"][unit_id]
            unit["power_on"] = not unit["power_on"]
            unit["last_event"] = str(datetime.now())
            self._toggle(unit)

            return Response.succ_response(self, unit)
