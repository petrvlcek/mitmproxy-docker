# Docker + [mitmproxy](https://mitmproxy.org/) = ❤️

[mitmproxy](https://mitmproxy.org/) is a very powerful interactive proxy for intercepting HTTP/HTTPS communication.

## Start the proxy

1. Clone this repository

2. Start the Docker container and mount the [scripts](./scripts) directory as a volume.

```bash
docker run --rm -it -p 8888:8080 -p 127.0.0.1:8889:8081 -v $(pwd)/scripts:/scripts  mitmproxy/mitmproxy mitmweb --web-iface 0.0.0.0 -s /scripts/noop.py
```

or just 

```bash
./run.sh
```

3. Open mitmproxy's web console in the browser: http://127.0.0.1:8889

4. Try it out

```
curl --proxy localhost:8888 -X GET http://old.host.com
```

## Basic scripts
Scripts can be used for intercepting requests passing throught the proxy. In the [scripts](./scripts) directory you can find some basic examples ready for use.

You can point to the script when starting the container and you can switch to another script any time later from the web console (in the Options). Scripts are also reloaded any time you modify them.

More examples are in mitmproxy's [GitHub repository]( https://github.com/mitmproxy/mitmproxy/tree/master/examples).

### Redirecting requests
```python
"""
This example shows two ways to redirect flows to another server.
"""
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # pretty_host takes the "Host" header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.
    if flow.request.pretty_host == "original.host.com":
        flow.request.host = "new.host.com"
```
