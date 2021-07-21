import grpc
import os
import spectroscope
import asyncio
from typing import List
from spectroscope.clients.beacon_client import BeaconChainStreamer
from spectroscope.clients.validator_client import ValidatorClientStreamer
from spectroscope.service.spectroscope_server import SpectroscopeServer
from proto_files.validator import service_pb2, service_pb2_grpc

from spectroscope.exceptions import NewKeys, ValidatorActivated, NewValidatorList

log = spectroscope.log()

class StreamingClient:
    """ Handles all the spectroscope app's features

    Args:
        validatorstream: stream validator info until its activation: activation epoch, its queue, and its status
        beaconstream: stream validator info per epoch: balances, and its status 
        rpcserver: serves users for validator list management: AddNodes, UpNodes and DelNodes available
    """
    def __init__(self,
        validatorstream: ValidatorClientStreamer,
        beaconstream: BeaconChainStreamer,
        rpcserver: SpectroscopeServer,
        unactive_validators: List[bytes],
        active_validators: List[bytes]=None,
    ):
        self.validatorstream = validatorstream
        self.beaconstream = beaconstream
        self.rpcserver = rpcserver
        self.unactive_validators = unactive_validators
        if active_validators is None:
            self.active_validators = []
        self.queue = asyncio.Queue(maxsize=1000)

    def setup(self):
        self.validatorstream.add_validators(set(map(bytes.fromhex, self.unactive_validators)))
        self.beaconstream.add_validators(set(map(bytes.fromhex, self.active_validators)))
        self.rpcserver.setup(self.queue)

    def _retrieve_keys(self):
        validators = self.rpcserver._retrieve_servicer().get_validators()
        return [key.validator_key.decode() for key in validators.validator]

    def _update_keys(self):
        self.validatorstream.add_validators(set(map(bytes.fromhex, self._retrieve_keys)))

    async def loop(self):
        while True:
            tasks = [i.stream() for i in [self.validatorstream,self.beaconstream] if i.count_validators()]
            tasks.append(self.rpcserver.serve())
            tasks.append(self.random_consumer(queue=self.queue))
            coros = [asyncio.create_task(task) for task in tasks]
            log.debug("task list checks part 1: before tasks{}".format(len(coros)))
            try:
                await asyncio.gather(*coros, return_exceptions=False)
            except ValidatorActivated as act:
                print("Activated Exception raised!")

                self.validatorstream.remove_validators(act.get_keys())
                self.beaconstream.add_validators(act.get_keys())
            except NewKeys as new_list:
                print("newKeys Exception raised!")
                validators_set = self.rpcserver.servicer.get_validators()
                self.validatorstream.update_validators(validators_set)
                self.beaconstream.update_validators(validators_set)
            except NewValidatorList as new_list:
                print("NewValidatorList Exception raised!")
                validators_set = self.rpcserver.servicer.get_validators()
                self.validatorstream.update_validators(validators_set)
            except KeyboardInterrupt:
                await self.rpcserver.stop()
                for t in tasks:
                    t.cancel()
                log.info("shutting down the server.. Goodbye !")
                break
            finally:
                await asyncio.sleep(1)

    async def random_consumer(self,queue):
        while True:
            msg = await queue.get()
            log.debug("Received a new message !!! {}".format(type(msg)))
            await asyncio.sleep(3)


#TODO create the graceful shutdown into restart to remove the runtime error for coroutines not awaited
    async def shutdown(self,tasks):
        log.info("Ending spectroscope, bye bye..")
        for t in tasks:
            t.cancel()
    
    #super hacky way to retrieve the whole list from the database 
    def _retrieve_keys(self):
        validators = self.rpcserver._retrieve_servicer().get_validators()
        return [key.validator_key.decode() for key in validators.validator]
    #back-up method that will reset the whole validator list
    def _rollback_keys(self):
        self.validatorstream.add_validators(self._retrieve_keys)

    def _update_keys(self,result):
        log.debug("updating the list with those keys: {}".format(result.get_keys()))
        self.validatorstream.remove_validators(result.get_keys())
        self.beaconstream.add_validators(result.get_keys())

    def _delete_keys(self, result):
        log.debug("deleting those keys: {}".format(result.get_keys()))
        self.validatorstream.remove_validators(result.get_keys())
        self.beaconstream.remove_validators(result.get_keys())

    def _add_keys(self, result):
        log.debug("adding those keys: {}".format(result.get_keys()))
        self.validatorstream.add_validators(result.get_keys())

    def _prompt_log(self,message):
        log.info("monitoring list modified: {}".format(message))