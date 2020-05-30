import websocket

class WebsocketClient:

    def  __init__(self):
        print("Spinning up WebsocketClient..")
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://localhost:8765",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        print("WebsocketClient running.")

    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        print("onopen client")
        self.ws.send('{"subscribe":["MSFT"]}')