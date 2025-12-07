import time
from backend.utils.crypto import sha256

class TXInput:
    def __init__(self, txid: str, index: int, signature: str):
        self.txid = txid
        self.index = index
        self.signature = signature

    def to_dict(self):
        return {
            "txid": self.txid,
            "index": self.index,
            "signature": self.signature
        }

class TXOutput:
    def __init__(self, amount: int, address: str):
        self.amount = amount
        self.address = address

    def to_dict(self):
        return {
            "amount": self.amount,
            "address": self.address
        }

class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = int(time.time())
        self.txid = self.hash()

    def serialize(self) -> str:
        return (
            "".join([f"{i.txid}{i.index}{i.signature}" for i in self.inputs]) +
            "".join([f"{o.amount}{o.address}" for o in self.outputs]) +
            str(self.timestamp)
        )

    def hash(self) -> str:
        return sha256(self.serialize())

    def to_dict(self):
        """序列化为 JSON 用于前端展示"""
        return {
            "txid": self.txid,
            "timestamp": self.timestamp,
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [o.to_dict() for o in self.outputs]
        }
