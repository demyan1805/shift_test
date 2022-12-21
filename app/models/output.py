from pydantic import BaseModel


class ContractEvent(BaseModel):
    args: dict
    event: str
    logIndex: int
    transactionIndex: int
    transactionHash: str
    address: str
    blockHash: str
    blockNumber: int
