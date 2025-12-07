from backend.blockchain.block import Block
from backend.blockchain.transaction import Transaction, TXOutput, TXInput
from backend.blockchain.utxo import UTXOSet


class Blockchain:
    """
    一个简单的 UTXO 区块链实现：
    - UTXOSet 始终只保存“已经上链”的状态
    - 普通交易进入 pending 时不立即修改 UTXO
    - 挖矿成功后，才一次性对区块中的所有交易应用 UTXO 变更
    """

    COINBASE_REWARD = 50

    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.utxos = UTXOSet()
        self.pending_transactions = []

        # 创世区块（无交易）
        self.chain.append(self.create_genesis_block())

    # -------------------------------
    # 创世区块
    # -------------------------------
    def create_genesis_block(self):
        genesis = Block(0, "0", [], self.difficulty)
        genesis.mine()
        return genesis

    def get_latest_block(self):
        return self.chain[-1]

    # -------------------------------
    # Step4: 挖矿（打包 pending + 奖励）
    # -------------------------------
    def mine_pending_transactions(self, miner_address: str):
        """
        挖矿流程：
        1. 构造 coinbase 奖励交易（不在这里更新 UTXO）
        2. coinbase + pending_transactions 打包成新区块
        3. PoW 挖矿
        4. 挖矿成功后，将区块加入链
        5. 对区块中的所有交易正式更新 UTXO
        6. 清空 pending 池
        """

        # 没有待打包交易也可以挖，只打奖励
        coinbase_tx = self.create_coinbase_tx(miner_address)

        # 当前区块包含：奖励交易 + 所有 pending 交易
        tx_list = [coinbase_tx] + list(self.pending_transactions)

        prev = self.get_latest_block()
        new_block = Block(prev.index + 1, prev.hash, tx_list, self.difficulty)

        print(f"Mining block {new_block.index} with {len(tx_list)} tx...")
        new_block.mine()

        # 区块写入链
        self.chain.append(new_block)

        # 正式应用交易对 UTXO 的影响
        self._apply_block_transactions(tx_list)

        # 清空 pending 池
        self.pending_transactions = []

        # 返回区块 JSON 给前端
        return new_block.to_dict()

    # -------------------------------
    # 应用区块中的所有交易到 UTXOSet
    # -------------------------------
    def _apply_block_transactions(self, tx_list):
        """
        对一个区块中的所有交易，统一更新 UTXO：
        - 对 coinbase 交易：只增加输出 UTXO
        - 对普通交易：花掉输入 UTXO，增加输出 UTXO
        """

        for tx in tx_list:
            # coinbase：没有 inputs
            if len(tx.inputs) == 0:
                # 只增加输出 UTXO
                for idx, out in enumerate(tx.outputs):
                    self.utxos.add_utxo(out.address, tx.txid, idx, out.amount)
            else:
                # 普通交易：需要花费若干 UTXO，再创建新的 UTXO
                selected = getattr(tx, "_selected_utxos", [])
                from_addr = getattr(tx, "from_address", None)

                # 1) 花掉输入对应的 UTXO
                if from_addr and selected:
                    for utxo in selected:
                        self.utxos.spend_utxo(from_addr, utxo["txid"], utxo["index"])

                # 2) 为每个输出创建新的 UTXO
                for idx, out in enumerate(tx.outputs):
                    self.utxos.add_utxo(out.address, tx.txid, idx, out.amount)

    # -------------------------------
    #   Chain 校验
    # -------------------------------
    def is_valid(self):
        """
        简单链校验：hash 连贯性 + 块内 hash 正确性。
        （UTXO 一致性未在此处校验）
        """
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # 当前区块 hash 是否被篡改
            if curr.hash != curr.calculate_hash():
                return False

            # 前向指针是否正确
            if curr.prev_hash != prev.hash:
                return False

        return True

    # -------------------------------
    #   Coinbase 交易 (奖励)
    # -------------------------------
    def create_coinbase_tx(self, miner_address: str) -> Transaction:
        """
        构造奖励交易：
        - 输入为空
        - 输出给 miner_address COINBASE_REWARD 个币
        ⚠️ 注意：这里只构造 Transaction，不修改 UTXO，
        真正修改在 _apply_block_transactions 里完成。
        """
        outputs = [TXOutput(self.COINBASE_REWARD, miner_address)]
        tx = Transaction([], outputs)
        return tx

    # -------------------------------
    #   Step3: 创建交易并加入 pending
    # -------------------------------
    def create_transaction(self, from_address, to_address, amount, signature="dummy"):
        """
        创建一笔普通交易流程：
        1. 从 UTXOSet 查询 from_address 可支配余额
        2. 若不足则返回 error
        3. 构造 TXInput/TXOutput
        4. 构造 Transaction 对象
        5. 挂载辅助信息（from_address, 选中的 UTXO 列表）
        6. 加入 pending_transactions
        ⚠️ 本函数不修改 UTXO，余额更新在挖矿成功后统一处理。
        """

        # 1. 查询可支配余额
        result = self.utxos.get_spendable(from_address, amount)
        if not result:
            return {"error": "Insufficient balance"}

        selected, total = result  # selected: 若干 UTXO; total: 这些 UTXO 总金额

        inputs = []

        # 2. 构造输入列表：引用哪些历史 UTXO
        for utxo in selected:
            txid = utxo["txid"]
            index = utxo["index"]
            inputs.append(TXInput(txid, index, signature))

        # 3. 构造输出列表：转给对方 + 找零
        outputs = [TXOutput(amount, to_address)]

        # 若总额大于本次转账金额，需要找零回给 from_address
        if total > amount:
            outputs.append(TXOutput(total - amount, from_address))

        tx = Transaction(inputs, outputs)

        # 4. 在交易对象上挂辅助信息，方便挖矿时更新 UTXO
        #    （Python 的对象是动态的，可以直接增加属性）
        tx.from_address = from_address
        tx._selected_utxos = selected

        # 5. 加入 pending
        self.pending_transactions.append(tx)

        # 6. 返回给前端 JSON
        return tx.to_dict()

    # -------------------------------
    # Step5: 返回整条链给前端
    # -------------------------------
    def get_chain(self):
        return [block.to_dict() for block in self.chain]
