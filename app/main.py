from fastapi import FastAPI
from web3 import Web3, HTTPProvider

from app.models.constants import NETWORKS_RPC
from app.api.routes import router


app = FastAPI()


@app.on_event("startup")
async def handle_startup():
    for network, rpc in NETWORKS_RPC.items():
        w3 = Web3(HTTPProvider(rpc))
        assert w3.isConnected()
        app.extra[network] = w3


app.include_router(router)
