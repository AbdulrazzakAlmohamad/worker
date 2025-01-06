from flask import request

from services.ResponseError import ResponseError


class Helper:

    def get_data():
        data = request.get_json()
        if not data:
            return ResponseError.DATA_NOT_FOUND

        return data
