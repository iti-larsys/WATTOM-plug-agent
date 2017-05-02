import aiohttp
import asyncio
import async_timeout
import grequests, time
import json, threading
from PublishSubscriber.Subscriber import Subscriber

class DataSender(Subscriber):
    def __init__(self, collectionEventURL, collectionDataURL):
        self.EventCollectionUrl = collectionEventURL
        self.DataCollectionUrl = collectionDataURL
        self.buffer = []
        self.dataSendSemaphore = threading.Semaphore(value=0)

    def sendDataEvent(self, data):
        """
        Function made to send events data when they are detected.
        :param payload:
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.askToSendEvent(loop, data))

    async def sendEvent(self, session, payload):
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.EventCollectionUrl,  headers=headers, data=json.dumps(payload)) as response:
                return

    async def askToSendEvent(self,loop, data):
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.sendEvent(session, data)
        except:
            print("Error sending")

    async def sendDataValues(self,session, payload):
        """
        Function made to send measured current and power values.
        :param payload:
        :return:
        """
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.DataCollectionUrl,  headers=headers, data=json.dumps(payload)) as response:
                return

    def callback_function(self, response):
        print("HTTP Response Code" + response.code)
        print("HTTP Response Headers" + response.headers)
        print("HTTP Response Body" + response.body)
        print("HTTP Response Raw Body" + response.raw_body)


    def requestException(self,request, exception):
        print("Unable to send data: " + str(exception))

    async def sendValues(self, loop, data):
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.sendDataValues(session, data)
        except:
            print("Error sending")

    def update(self,data):
        print("Going to send power data")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.sendValues(loop, data))
        # print("Going to send power data")
        # self.buffer.append(data)
        # self.dataSendSemaphore.release()

"""
if __name__ == "__main__":
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/continuous_measuring"
    object = dataSender(url1, url2)

    while True:
        print("Sending Data Events")
        object.sendDataEvent({'type': "on", 'timestamp': str(time.time())})
        #object.sendDataValues({'power':'1024', 'current':'10', 'timestamp': str(time.time())})
"""