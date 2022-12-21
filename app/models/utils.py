from web3.datastructures import AttributeDict
from hexbytes import HexBytes


def encoded_dict(attr_dict: AttributeDict) -> dict:
    new_dict = {}

    for k, v in attr_dict.items():
        if isinstance(v, AttributeDict):
            new_dict[k] = encoded_dict(v)
        elif isinstance(v, HexBytes) or isinstance(v, bytes):
            new_dict[k] = v.hex()
        else:
            new_dict[k] = v

    return new_dict
