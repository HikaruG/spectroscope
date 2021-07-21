import grpc
from concurrent import futures
import sys, os
sys.path.append(os.path.dirname(os.path.abspath("app.py")))
from proto_files.validator import service_pb2_grpc
from spectroscope.service.rpc_responder import RPCValidatorServicer
from spectroscope.module import Module
from typing import List, Set, Tuple, Type
from spectroscope.exceptions import NewValidatorList,NewKeys
import spectroscope
import asyncio
log = spectroscope.log()

class SpectroscopeServer:
  """ Handles all the spectroscope app's features

    Args:
        validatorstream: stream validator info until its activation: activation epoch, its queue, and its status
        beaconstream: stream validator info per epoch: balances, and its status 
        rpcserver: serves users for validator list management: AddNodes, UpNodes and DelNodes available
    """
  def __init__(
    self,
    host: str,
    port: int,
    modules: List[Tuple[Type[Module], dict]],
  ):
    self.host = host
    self.port = port
    self.modules = modules
    self.server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    
    self.server.add_insecure_port('{}:{}'.format(host,port))
  
  def setup(self, queue:asyncio.Queue):
    servicer = RPCValidatorServicer(queue=queue ,modules=self.modules)
    service_pb2_grpc.add_ValidatorServiceServicer_to_server(
        servicer,self.server
    )

  async def serve(self):
    await self.server.start()

  
  async def stop(self):
    await self.server.stop(grace=None)