import asyncio
import websockets
import json
import requests

class WebsocketServer:

    def  __init__(self):
        print("Starting WebsocketServer...")
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.echo, 'localhost', 8765))
        asyncio.get_event_loop().run_forever()


    async def echo(self, websocket, path):
        print("echo server")
        async for message in websocket:
            print("Loading " + json.loads(message)["subscribe"][0] + " data..")
            self.readFromEndpoint(json.loads(message)["subscribe"][0], '1m', '7d')
            parsedData = self.parseJsonData()
            indicators = parsedData[0]
            timestamp = parsedData[1]
            for i in range(0, len(indicators["volume"]) - 1):
                if indicators["high"][i] != None:
                    await websocket.send('{'
                                        + ' "timestamp": ' + '"' + str(timestamp[i]) + '", '
                                        + ' "volume": ' + '"' + str(indicators["volume"][i]) + '", '
                                        + '"high": ' + '"' + str(indicators["high"][i]) + '", '
                                        + '"low": ' + '"' + str(indicators["low"][i]) + '", '
                                        + '"close": ' + '"' + str(indicators["close"][i]) + '", '
                                        + '"open": ' + '"' + str(indicators["open"][i])
                                        + '" }')


    # Read data from a file
    def readFile(file_name):
        # Opening JSON file
        f = open('../resources/' + file_name, )
        # returns JSON object as a dictionary
        data = json.load(f)
        f.close()
        return data


    # Pull data from the endpoint with a simple http request.
    def readFromEndpoint(self, security, interval, range):
        r = requests.get(
            'https://query1.finance.yahoo.com/v8/finance/chart/' + security + '?includePrePost=false&interval=' + interval + '&range=' + range + '&corsDomain=finance.yahoo.com&.tsrc=finance')
        self.data = json.loads(r.content)


    # Get the data we want out of the object retrieved from the endpoint.
    def parseJsonData(self):
        indicators = self.data["chart"]["result"][0]["indicators"]["quote"][0]
        timestamp = self.data["chart"]["result"][0]["timestamp"]
        return (indicators, timestamp)


    # Print data line by line in json format
    # For testing purposes.
    def printLines(indicators, timestamp):
        for i in range(0, len(indicators["volume"]) - 1):
            print('{'
                + ' "timestamp": ' + '"' + str(timestamp[i]) + '", '
                + ' "volume": ' + '"' + str(indicators["volume"][i]) + '", ' + '"high": ' + '"' + str(indicators["high"][i]) + '", '
                + '"low": ' + '"' + str(indicators["low"][i]) + '", ' + '"close": ' + '"' + str(indicators["close"][i]) + '", '
                + '"open": ' + '"' + str(indicators["open"][i])
                + '" }')