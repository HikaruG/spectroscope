import requests, json
from spectroscope.model import Action
from spectroscope.model.notification import Notify
from spectroscope.module import ConfigOption, Plugin
from typing import List
import spectroscope
log = spectroscope.log()

class Webhook(Plugin):
    _consumed_types = [Notify]

    config_options = [
        ConfigOption(
            name="uri_endpoint",
            param_type=str,
            description="Endpoint to call webhook from",
        ),
        ConfigOption(
            name="webhook_type",
            param_type=int,
            description="type of webhook: 1=REST,2=GRAPHQL",
        ),
        ConfigOption(
            name="query_details",
            param_type=str,
            description="Query format: you must put __message__ to indicate where spectroscope puts notification data"
        )
    ]

    def __init__(self, uri_endpoint: str,webhook_type:int, query_details:str):
        self._uri_endpoint = uri_endpoint
        self.webhook_type = webhook_type
        self.query_details = query_details
        self._handlers = {
            1: self._rest,
            2: self._graphql
        }

    @classmethod
    def register(cls, **kwargs):
        return cls(
            kwargs["uri_endpoint"],
            kwargs["webhook_type"],
            kwargs["query_details"],
            )

    def consume(self, events: List[Action]):
        for event in events:
            self._handlers[self.webhook_type](event.notification.get_str_dict())
            

    def _rest(self, validator_info):
        r = requests.post(
                self._uri_endpoint, json=validator_info
            )
        print(r.content)
        print(r.status_code)

    def _graphql(self,validator_info):
        event_keys = [keys for keys in validator_info]
        event_str = json.dumps(validator_info)
        for key in event_keys:
            event_str = event_str.replace('"{}"'.format(key),key)
        r = requests.post(
                self._uri_endpoint, json={"query":self.query_details.replace("__message__",event_str)}
            )
        print(r.content)
        print(r.status_code)