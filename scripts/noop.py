"""
This script passes the flow through without any actions.
"""
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # this script does nothing
    return
