docker run --name mitmproxy --rm -d -p 192.168.0.100:8888:8080 -p 127.0.0.1:8889:8081 -v $(pwd):/data  mitmproxy/mitmproxy mitmweb --web-host 0.0.0.0 --web-port 8081 -s /data/scripts/redirect.py -s /data/scripts/modify_response.py
docker logs mitmproxy -f
