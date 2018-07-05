"""
This example shows how to modify responses.
"""
from types import FunctionType
from mitmproxy import http, ctx
import json
import os
import re

# Replacement rules
rules = {
    ".*/users/.*": {
        "status_code": 400,
        "content": lambda: file("invalid_token.json"), # you can use a lambda and load the response from a json file located in /content folder
    },
    "/.*": { # match URL with a regular expression
        "status_code": 503, # replace response code
        "content": '{"error": "service_unavailable"}', # replace content
    },
}

# this is called for incoming request before sending to the destination host
def request(flow: http.HTTPFlow) -> None:
    ctx.log.info("Request domain: " + flow.request.pretty_host +
                 ", path: " + flow.request.path)


# this is called for a response before returning to the proxy client
def response(flow: http.HTTPFlow) -> None:
    if 'content-type' in flow.response.headers and flow.response.headers["content-type"].startswith("application/json"):
        for rule in rules:
            if re.match(rule, flow.request.path) is not None:
                ctx.log.info("Matched path for replacement: " +
                             flow.request.path)
                replaceResponse(flow, rules[rule])
                break # use first matched rule


def replaceResponse(flow: http.HTTPFlow, rule: dict) -> None:
    ctx.log.info("Original status: " + str(flow.response.status_code))
    if "status_code" in rule:
        flow.response.status_code = rule["status_code"]
        ctx.log.info("Replaced status: " + str(flow.response.status_code))

    ctx.log.info("Original response body: " +
                 flow.response.content.decode("utf-8"))
    if "content" in rule:
        if isinstance(rule["content"], FunctionType):
            flow.response.content = rule["content"]().encode("utf-8")
        else:
            flow.response.content = rule["content"].encode("utf-8")

        ctx.log.info("Replaced response body: " +
                     flow.response.content.decode("utf-8"))


def file(filename: str) -> str:
    file_path = os.path.join("/data/content", filename)
    with open(file_path) as json_file:
        json_data = json.load(json_file)
        return json.dumps(json_data)
