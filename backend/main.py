from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet

# 初始化 Flask
app = Flask(__name__)
CORS(app)

# 初始化区块链
bc = Blockchain(difficulty=4)

# ------------------------------
# Step5: 获取整条链
# ------------------------------
@app.get("/blocks")
def get_blocks():
    return jsonify(bc.get_chain())


# ------------------------------
# Step3: 创建交易
# ------------------------------
@app.post("/transaction")
def create_tx():
    data = request.json

    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")
    signature = data.get("signature", "dummy")  # 暂时还没启用真实签名

    tx = bc.create_transaction(sender, receiver, amount, signature)

    return jsonify(tx)


# ------------------------------
# Step4: 挖矿
# ------------------------------
@app.post("/mine")
def mine_block():
    data = request.json or {}
    miner_addr = data.get("miner", "MINER001")

    new_block = bc.mine_pending_transactions(miner_addr)

    return jsonify({
        "status": "success",
        "block": new_block
    })


# ------------------------------
# 生成钱包
# ------------------------------
@app.get("/create_wallet")
def create_wallet():
    wallet = Wallet()
    return jsonify({
        "private_key": wallet.export_private_key(),
        "public_key": wallet.export_public_key(),
        "address": wallet.get_address()
    })


# ------------------------------
# 查询余额
# ------------------------------
@app.get("/balance/<address>")
def get_balance(address):
    balance = bc.utxos.get_balance(address)
    return jsonify({
        "address": address,
        "balance": balance
    })


# ------------------------------
# 查看 pending tx
# ------------------------------
@app.get("/pending")
def get_pending():
    return jsonify([tx.to_dict() for tx in bc.pending_transactions])


# ------------------------------
# 入口
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
