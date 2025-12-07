from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet

app = Flask(__name__)
CORS(app)

# 初始化区块链
bc = Blockchain(difficulty=4)


# ====================================================
# 获取完整区块链（Step5 + 可视化 + 交易详情）
# ====================================================
@app.get("/blocks")
def get_blocks():
    return jsonify(bc.get_chain())


# ====================================================
# 创建交易（前端手动 or 作为基础接口）
# body: { "sender", "receiver", "amount", "signature" }
# ====================================================
@app.post("/transaction")
def create_transaction():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")
    signature = data.get("signature", "dummy")

    tx = bc.create_transaction(sender, receiver, amount, signature)

    # create_transaction 已经返回 dict（要么 error，要么 tx dict）
    return jsonify(tx)


# ====================================================
# 挖矿（包含 coinbase 奖励）
# body: { "miner": "<address>" }
# ====================================================
@app.post("/mine")
def mine():
    data = request.json or {}
    miner = data.get("miner", "MINER001")

    new_block = bc.mine_pending_transactions(miner)

    return jsonify({
        "status": "success",
        "block": new_block
    })


# ====================================================
# 生成钱包
# ====================================================
@app.get("/create_wallet")
def create_wallet():
    w = Wallet()
    return {
        "private_key": w.export_private_key(),
        "public_key": w.export_public_key(),
        "address": w.get_address()
    }


# ====================================================
# 根据私钥恢复钱包（导入钱包）
# body: { "private_key": "..." }
# ====================================================
@app.post("/create_wallet_from_key")
def create_wallet_from_key():
    data = request.json
    private_key = data["private_key"]

    wallet = Wallet.from_private_key(private_key)

    return {
        "private_key": wallet.export_private_key(),
        "public_key": wallet.export_public_key(),
        "address": wallet.get_address()
    }


# ====================================================
# 余额查询
# ====================================================
@app.get("/balance/<address>")
def balance(address):
    bal = bc.utxos.get_balance(address)
    return {"address": address, "balance": bal}


# ====================================================
# pending 交易查看（Mempool 监控）
# ====================================================
@app.get("/pending")
def pending():
    return jsonify([tx.to_dict() for tx in bc.pending_transactions])


# ====================================================
# 使用私钥自动创建并签名交易（SendTransaction 用）
# body: { "private_key", "from", "to", "amount" }
# ====================================================
@app.post("/tx/create_signed")
def create_signed_tx():
    data = request.json

    private_key = data["private_key"]
    from_addr = data["from"]
    to_addr = data["to"]
    amount = data["amount"]

    # 私钥恢复钱包
    w = Wallet.from_private_key(private_key)

    # 自动生成 message
    message = f"{from_addr}{to_addr}{amount}"

    # 自动签名
    signature = w.sign(message)
    public_key = w.export_public_key()

    tx = bc.create_transaction(
        from_addr,
        to_addr,
        amount,
        signature
    )

    if "error" in tx:
        return jsonify({"status": "fail", "msg": tx["error"]})

    return jsonify({
        "status": "success",
        "tx": tx,
        "public_key": public_key,
        "signature": signature
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
