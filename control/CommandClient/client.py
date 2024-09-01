#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

from . import libclient

class Client:
    def __init__(self, host, port, callback):
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.callback = callback

    def create_request(self, data):
        return dict(
            type="text/json",
            encoding="utf-8",
            content=data,
        )

    def sendMessage(self, data):
        msg = self.create_request(dict(data))
        self._start_connection(msg)

    def _start_connection(self, request):
        addr = (self.host, self.port)
        print("starting connection to", addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(addr)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.message = libclient.Message(self.sel, self.sock, addr, request, self.callback)
        self.sel.register(self.sock, self.events, data=self.message)

        try:
            while True:
                self.events = self.sel.select(timeout=1)
                for key, mask in self.events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

def callback(response):
    print("callback got response")
    print(response)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("usage:", sys.argv[0], "<host> <port> <action> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    action, value = sys.argv[3], sys.argv[4]

    client = Client(host, port)
    data = {'action':action, 'value':value}
    client.sendMessage(data)