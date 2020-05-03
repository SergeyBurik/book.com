# coding: utf-8
import json


def decode_response(data):
    return json.loads(data.decode('utf-8'))


