import os
import json


def read_config() -> dict:
    with open("./conf.json", "r") as f:
        return json.loads(f.read())
