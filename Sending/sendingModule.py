import asyncio
import json
import threading

import aiohttp
import async_timeout

from PublishSubscriber.Subscriber import Subscriber


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyBroadException,PyBroadException
class DataSender(Subscriber):
    def __init__(self, collection_event_url, collection_data_url):
        self.EventCollectionUrl = collection_event_url
        self.DataCollectionUrl = collection_data_url
        self.buffer = []
        self.dataSendSemaphore = threading.Semaphore(value=0)

    def send_data_event(self, data):
        """
        Function made to send events data when they are detected.
        :param data:
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ask_to_send_event(loop, data))

    async def send_event(self, session, payload):
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.EventCollectionUrl, headers=headers, data=json.dumps(payload)) as response:
                return

    async def ask_to_send_event(self, loop, data):
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.send_event(session, data)
        except:
            print("Error sending")

    async def send_data_values(self, session, payload):
        """
        Function made to send measured current and power values.
        :param session:
        :param payload:
        :return:
        """
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.DataCollectionUrl, headers=headers, data=json.dumps(payload)) as response:
                return

    def callback_function(self, response):
        print("HTTP Response Code" + response.code)
        print("HTTP Response Headers" + response.headers)
        print("HTTP Response Body" + response.body)
        print("HTTP Response Raw Body" + response.raw_body)

    def request_exception(self, request, exception):
        print("Unable to send data: " + str(exception))

    async def send_values(self, loop, data):
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.send_data_values(session, data)
        except:
            print("Error sending")

    def update(self, data):
        print("Going to send power data")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_values(loop, data))
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
