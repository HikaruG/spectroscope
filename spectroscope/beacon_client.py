from ethereumapis.v1alpha1 import beacon_chain_pb2, beacon_chain_pb2_grpc
from spectroscope.model.base import ChainTimestamp, ValidatorIdentity
from spectroscope.model.update import (
    ValidatorBalanceUpdate,
    ValidatorStatusUpdate,
    UpdateBatch,
)
from spectroscope.module import Module
from spectroscope.module.plugin import BasePlugin
from spectroscope.module.subscriber import Subscriber
from typing import List, Set, Tuple, Type


class BeaconChainStreamer:
    def __init__(
        self,
        stub: beacon_chain_pb2_grpc.BeaconChainStub,
        modules: List[Tuple[Type[Module], dict]],
    ):
        self.stub = stub
        self.subscribers = list()
        self.plugins = list()
        self.validator_set = set()

        for module, config in modules:
            if issubclass(module, Subscriber):
                self.subscribers.append(module().register(**config))
            elif issubclass(module, BasePlugin):
                self.plugins.append(module().register(**config))
            else:
                raise TypeError

    def add_validators(self, validators: Set[bytes]):
        for validator in validators:
            self.validator_set.add(validator)

    def remove_validators(self, validators: Set[bytes]):
        for validator in validators:
            self.validator_set.remove(validator)

    def register_subscriber(self, subscriber: Subscriber):
        subscriber.register()
        self.subscribers.append(subscriber)

    def register_plugin(self, plugin: BasePlugin):
        plugin.register()
        self.plugins.append(plugin)

    def _generate_messages(self):
        yield beacon_chain_pb2.ValidatorChangeSet(
            action=beacon_chain_pb2.SET_VALIDATOR_KEYS,
            public_keys=self.validator_set,
        )

    def stream_responses(self, stream):
        for validator_info in stream:
            updates = [
                ValidatorStatusUpdate(status=validator_info.status),
                ValidatorBalanceUpdate(
                    balance=validator_info.balance,
                    effectiveBalance=validator_info.effective_balance,
                ),
            ]

            responses = list()
            for subscriber in self.subscribers:
                batch = UpdateBatch(
                    validator=ValidatorIdentity(
                        pubkey=validator_info.public_key, idx=validator_info.index
                    ),
                    timestamp=ChainTimestamp(epoch=validator_info.epoch, slot=0),
                    updates=list(
                        filter(lambda x: type(x) in subscriber.consumed_types, updates)
                    ),
                )
                responses.extend(subscriber.consume(batch))

            for plugin in self.plugins:
                plugin.consume(
                    list(filter(lambda x: type(x) in sink.consumed_types, responses))
                )

    def stream(self):
        self.stream_responses(self.stub.StreamValidatorsInfo(self._generate_messages()))