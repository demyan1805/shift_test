from functools import reduce
from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
)
from starlette import status
from web3 import Web3
from web3.contract import ContractEvent

from app.models.input import GetBalanceReq, GetEventsReq
from app.models.output import ContractEvent
from app.models.enums import Networks
from app.models.constants import EVENTS_CONTRACT, EVENTS_CONTRACT_ABI
from app.models.utils import encoded_dict
from app.services.snowtrace import SnowtraceAPI


router = APIRouter(prefix="/api")


@router.get("/balance")
async def get_balance(
    request: Request,
    req_data: GetBalanceReq = Depends(),
):
    w3 = request.app.extra[req_data.network]

    try:
        addr = Web3.toChecksumAddress(req_data.address)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid address",
        )

    return w3.eth.get_balance(
        addr,
        req_data.block_number,
    )


@router.get("/contract_events", response_model=list[ContractEvent])
async def get_contract_events(
    request: Request,
    req_data: GetEventsReq = Depends(),
):
    w3 = request.app.extra[Networks.AVAX]

    contract_addr = EVENTS_CONTRACT
    contract_abi = EVENTS_CONTRACT_ABI
    if req_data.contract is not None:
        snowtrace_api = SnowtraceAPI()
        contract_addr = req_data.contract
        contract_abi = await snowtrace_api.get_contract_abi(req_data.contract)

    contract = w3.eth.contract(
        address=contract_addr,
        abi=contract_abi,
    )
    return reduce(
        lambda acc, event: [
            *acc,
            *list(map(
                lambda eventLog: ContractEvent(**encoded_dict(eventLog)),
                event.getLogs(
                    fromBlock=req_data.from_block,
                    toBlock=req_data.to_block,
                ),
            )),
        ],
        contract.events,
        [],
    )
