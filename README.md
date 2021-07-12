# Docker + [mitmproxy](https://mitmproxy.org/) = ❤️

[mitmproxy](https://mitmproxy.org/) is a very powerful interactive proxy for intercepting HTTP/HTTPS communication.

## Start the proxy

1. Clone this repository

```bash
git clone git@github.com:petrvlcek/mitmproxy-docker.git
cd mitmproxy-docker
```

2. Start the Docker container and mount project root as a `/data` volume.

```bash
docker run --name mitmproxy --rm -d -p 8888:8080 -p 127.0.0.1:8889:8081 -v $(pwd):/data  mitmproxy/mitmproxy mitmweb --web-host 0.0.0.0 --web-port 8081 -s /data/scripts/redirect.py -s /data/scripts/modify_response.py
docker logs mitmproxy -f
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

## Example scripts
Scripts can be used for intercepting requests passing throught the proxy. In the [scripts](./scripts) directory you can find some basic examples ready for use.

You can point to the script (or multiple scripts) when starting the container and you can switch to another script any time later from the web console (in the Options). Scripts are also reloaded whenever you modify them.


1. [Redirecting requests](./scripts/redirect.py)
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
2. [Response modification](./scripts/modify_response.py)

More examples are in mitmproxy's [GitHub repository]( https://github.com/mitmproxy/mitmproxy/tree/master/examples).
