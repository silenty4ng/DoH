"""
/*
 * @Author: Silent YANG 
 * @Date: 2023-11-29
 */
"""

from flask import Flask, request, make_response
from base64 import urlsafe_b64decode
import socket

app = Flask(__name__)
socket.setdefaulttimeout(5)

@app.route("/dns-query" ,methods=['GET', 'POST'])
def dns_query():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if request.headers.get('CONTENT_TYPE') == 'application/dns-message':
        sock.sendto(request.stream.read(), ("1.1.1.1", 53))
        rx_meesage, addr = sock.recvfrom(4096)
        return make_response(rx_meesage, 200, {"Content-Type": "application/dns-message"})
    if request.method == "GET" and request.args.get("dns"):
        payload = urlsafe_b64decode(request.args.get("dns") + "===")
        sock.sendto(payload, ("1.1.1.1", 53))
        rx_meesage, addr = sock.recvfrom(4096)
        return make_response(rx_meesage, 200, {"Content-Type": "application/dns-message"})
    sock.close()
    return make_response("", 400)

if __name__ == "__main__":
    app.run('127.0.0.1', debug=False, port=5000)
