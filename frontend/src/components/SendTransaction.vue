<template>
  <div class="page-section">
    <h2 class="page-title">发送交易</h2>

    <el-card class="app-card">
      <div class="card-body">

        <!-- 输入表单 -->
        <div class="form-row">
          <label class="label">接收方地址</label>
          <el-input
            v-model="to_addr"
            placeholder="请输入接收方钱包地址"
            class="input"
          />
        </div>

        <div class="form-row">
          <label class="label">金额（BTC）</label>
          <el-input
            v-model.number="amount"
            type="number"
            placeholder="请输入转账金额"
            class="input"
          />
        </div>

        <div class="btn-row">
          <el-button type="primary" @click="sendTransaction()">
            提交交易
          </el-button>
        </div>

        <div v-if="txid" class="result-box">
          <p class="result-title">交易提交成功</p>
          <p class="mono small">{{ txid }}</p>
          <p class="subtext">
            请前往区块链页面挖矿确认交易。
          </p>
        </div>

      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      to_addr: "",
      amount: null,
      txid: null,
      wallet: null,
    }
  },

  methods: {
    async sendTransaction() {
      if (!this.wallet)
        return alert("请先创建或选择钱包！")

      if (!this.to_addr || this.amount === null || this.amount <= 0)
        return alert("请输入合法的转账金额与地址！")

      const body = {
        private_key: this.wallet.private_key,
        from: this.wallet.address,
        to: this.to_addr,
        amount: Number(this.amount)
      }

      try {
        const res = await axios.post("http://127.0.0.1:5000/tx/create_signed", body)

        if (res.data.status === "success") {
          // 正确读取 txid
          this.txid = res.data.tx.txid

          this.to_addr = ""
          this.amount = null

          alert("交易已提交！（等待挖矿确认）")
        } else {
          alert("交易失败：" + res.data.msg)
        }
      } catch (e) {
        alert("请求失败：" + e)
      }
    },
  },

  mounted() {
    const saved = JSON.parse(localStorage.getItem("wallets") || "[]")
    const addr = localStorage.getItem("currentWallet")
    this.wallet = saved.find((w) => w.address === addr) || null
  },
}
</script>


<style scoped>
.page-section {
  margin-bottom: 24px;
}

.page-title {
  font-size: 36px;
  margin-bottom: 18px;
}

/* 表单块 */
.form-row {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 18px;
  font-weight: 500;
  color: #050510;
  margin-bottom: 20px;
}

/* 输入框字体颜色 */
:deep(.el-input__inner) {
  color: #050510 !important;
  font-size: 18px;
}

/* 提交按钮区 */
.btn-row {
  margin-top: 12px;
}

/* 提交结果 */
.result-box {
  margin-top: 22px;
  padding: 16px;
  border-radius: 10px;
  background: #f1f1f4;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  color: #050510;
  margin-bottom: 6px;
}

.mono {
  font-family: "JetBrains Mono", monospace;
  color: #050510;
  word-break: break-all;
}

.small {
  font-size: 13px;
}

.subtext {
  margin-top: 6px;
  color: #050510;
  opacity: 0.75;
  font-size: 12px;
}
</style>
