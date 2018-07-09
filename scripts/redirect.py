"""
This example shows two ways to redirect flows to another server.
"""
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # pretty_host takes the "Host" header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.
    if flow.request.pretty_host == "api.example.com":
        flow.request.host = "192.168.0.1"
        flow.request.port = 8080