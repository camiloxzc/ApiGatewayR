import re
from flask import request

def format_url():
    parts = request.path.split("/")
    url = request.path
    for part in parts:
        if re.search('\\d', parts):
            url = url.replace(part, "?")
    return url