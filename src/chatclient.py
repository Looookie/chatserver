'''
Created on 2018年3月6日

@author: Luke
'''

import logging

import websocket
from threading import Thread
import time
import sys
import json

SERVER_URL = 'ws://localhost:8000/chat'

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):

    def run(*args):
        for i in range(10):
            data = {'message' : 'Hello %d' % i}
            ws.send(json.dumps(data))
            time.sleep(1)

        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(SERVER_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
