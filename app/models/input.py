from typing import Optional, Literal

from fastapi import HTTPException
from pydantic import BaseModel, conint, root_validator
from starlette import status

from .enums import Networks


class GetBalanceReq(BaseModel):
    address: str
    block_number: Optional[conint(ge=0)]
    network: Optional[Networks] = Networks.AVAX


class GetEventsReq(BaseModel):
    from_block: conint(ge=0)
    to_block: Optional[conint(ge=0)]
    contract: Optional[str]

    @root_validator
    def block_range_validator(cls, data):
        if data.get('to_block') and data['to_block'] < data['from_block']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="negative block range",
            )
        return data
