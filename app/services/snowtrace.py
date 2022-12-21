from httpx import AsyncClient
from fastapi import HTTPException
from starlette import status


class SnowtraceAPI:
    BASE_URL = "https://api.snowtrace.io/api"


    async def get_contract_abi(self, address) -> dict:
        async with AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                self.BASE_URL,
                params={
                    "module": "contract",
                    "action": "getabi",
                    "address": address,
                    "format": "raw",
                }
            )
            if resp.status_code // 2 != 100:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="snowtrace api error"
                )

            data = resp.json()
            # wierd snowtrace api returns 200 even if has error
            if isinstance(data, dict) and data.get("message") == "NOTOK":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=data.get("result"),
                )
            return data
