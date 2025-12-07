import time
from backend.utils.crypto import sha256

class Block:
    def __init__(self, index, prev_hash, transactions, difficulty):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions  # list[Transaction]
        self.timestamp = int(time.time())
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = ""

    def calculate_hash(self):
        """
        区块哈希由：index + prev_hash + timestamp + 所有交易ID + nonce 组成
        """
        tx_str = "".join(tx.txid for tx in self.transactions)
        block_str = f"{self.index}{self.prev_hash}{self.timestamp}{tx_str}{self.nonce}"
        return sha256(block_str)

    def mine(self):
        """
        基于 difficulty 进行工作量证明挖矿
        """
        print(f"⛏ Mining block {self.index} ...")
        target = "0" * self.difficulty

        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                print(f"✔ Block {self.index} mined with hash: {self.hash}")
                break
            self.nonce += 1

    def to_dict(self):
        """
        变成 JSON 可序列化格式（提供给前端）
        """
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }
