import json
import logging
import os
from uuid import uuid4

from py_s2s.s2s_client import RMQClient
from py_s2s.s2s_connection_config import RabbitConfig

logging.basicConfig(level=str(os.getenv('S2S_LOGLEVEL', 'info')).upper())
logger = logging.getLogger(__name__)


class Service2Service:
    def __init__(self, service_name: str, config: RabbitConfig):
        self.config = config
        self.client = None
        self.service_name = service_name

    async def request(self, path: str, body: dict, headers: dict = None):
        """
        Send http-style request over rabbit. (You need to use a service that serves http over rabbit)
        :param path: string, this is the request path
        :param body: dictionary, will become json over rmq
        :param headers: dictionary, http-headers accepted
        :return: Response object from rabbit
        """
        if not self.client:
            self.client = RMQClient(self.service_name, self.config.exchange, self.config.queue_name)
            await self.client.connect(config=self.config)
            # await self.client.bind(path)
        if headers is None:
            headers = {}

        headers['accept-encoding'] = ''  # keep it from gzip'ing the response (it's rabbitmq afterall)
        correlation_id = str(uuid4())
        if 'x-correlation-id' not in headers.keys():
            headers['x-correlation-id'] = correlation_id

        rabbit_path = path.strip('/').replace('/', '.')
        result = await self.client.send_request(rabbit_path, json=body, headers=headers)
        result.body = json.loads(result.body)
        return result
