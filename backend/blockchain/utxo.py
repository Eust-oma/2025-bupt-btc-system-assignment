class UTXOSet:
    def __init__(self):
        # mapping: address → list of {txid, index, amount}
        self.utxos = {}

    # ----------------------------------------
    # 添加 UTXO
    # ----------------------------------------
    def add_utxo(self, address, txid, index, amount):
        if amount <= 0:
            return
        if address not in self.utxos:
            self.utxos[address] = []
        self.utxos[address].append({
            "txid": txid,
            "index": index,
            "amount": amount
        })

    # ----------------------------------------
    # 移除 UTXO（作为输入使用后）
    # ----------------------------------------
    def spend_utxo(self, address, txid, index):
        if address not in self.utxos:
            return
        self.utxos[address] = [
            u for u in self.utxos[address]
            if not (u["txid"] == txid and u["index"] == index)
        ]

    # ----------------------------------------
    # 获取余额
    # ----------------------------------------
    def get_balance(self, address):
        if address not in self.utxos:
            return 0
        return sum(u["amount"] for u in self.utxos[address])

    # ----------------------------------------
    # 查找可支付金额的 UTXO 集（返回 UTXO 列表与总额）
    # ----------------------------------------
    def get_spendable(self, address, amount):
        """查找足够支付 amount 的 UTXO 集"""
        if address not in self.utxos:
            return None

        if amount <= 0:
            return None

        selected = []
        total = 0

        # 简单线性搜索
        for utxo in self.utxos[address]:
            selected.append(utxo)
            total += utxo["amount"]
            if total >= amount:
                return selected, total

        return None

    # ----------------------------------------
    # 扩展：返回某地址所有 UTXO （前端显示余额可用）
    # ----------------------------------------
    def get_address_utxos(self, address):
        return self.utxos.get(address, [])

    # ----------------------------------------
    # 扩展：整体状态序列化（调试用）
    # ----------------------------------------
    def to_dict(self):
        return self.utxos
