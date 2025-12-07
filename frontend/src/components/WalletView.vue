<template>
  <div class="page-section">
    <h2 class="page-title">钱包</h2>

    <!-- 无钱包状态 -->
    <el-card v-if="!wallet" class="app-card">
      <div class="card-body empty-state">
        <p class="empty-title">当前没有已选择的钱包</p>
        <p class="subtext">
          请点击右上角导航栏中的「钱包列表」按钮进行创建或导入钱包。
        </p>
        <el-button type="primary" @click="openManager">打开钱包列表</el-button>
      </div>
    </el-card>

    <!-- 有钱包状态 -->
    <el-card v-else class="app-card">
      <div class="card-body">
        <div class="wallet-header">
          <div class="section-title">当前钱包</div>
          <span class="tag-label">浏览器本地保存，不上传服务器</span>
        </div>

        <el-descriptions :column="1" size="small" class="wallet-desc">
          <el-descriptions-item label="当前矿工">
            <strong>{{ wallet.address }}</strong>
          </el-descriptions-item>

          <el-descriptions-item label="地址">
            <span class="mono">{{ wallet.address }}</span>
          </el-descriptions-item>

          <el-descriptions-item label="公钥">
            <span class="mono">{{ wallet.public_key }}</span>
          </el-descriptions-item>

          <el-descriptions-item label="私钥">
            <span class="mono">
              {{ wallet.private_key }}
              <span class="subtext-inline">（请勿泄露，仅 Demo 环境显示）</span>
            </span>
          </el-descriptions-item>

          <el-descriptions-item label="余额">
            <strong>{{ balance }} BTC</strong>
          </el-descriptions-item>
        </el-descriptions>

        <div class="btn-row">
          <el-button @click="loadBalance" :loading="loadingBalance">
            刷新余额
          </el-button>

          <el-button
            type="primary"
            @click="mineReward"
            :loading="mining"
          >
            挖矿奖励给我
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios"

export default {
  props: {
    currentWallet: {
      type: Object,
      default: null
    }
  },

  emits: ["openWalletManager"],

  data() {
    return {
      wallet: null,
      balance: 0,
      loadingBalance: false,
      mining: false,
    }
  },

  watch: {
    currentWallet: {
      immediate: true,
      handler(newVal) {
        this.wallet = newVal
        if (this.wallet) {
          this.loadBalance()
        } else {
          this.balance = 0
        }
      }
    }
  },

  methods: {
    openManager() {
      this.$emit("openWalletManager")
    },

    async loadBalance() {
      if (!this.wallet) return
      this.loadingBalance = true

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/balance/${this.wallet.address}`
        )
        this.balance = res.data.balance
      } finally {
        this.loadingBalance = false
      }
    },

    async mineReward() {
      if (!this.wallet) {
        return this.$message.warning("请先选择钱包")
      }
      this.mining = true
      try {
        await axios.post("http://127.0.0.1:5000/mine", {
          miner: this.wallet.address,
        })
        this.$message.success("挖矿成功！奖励已发放到钱包")
        this.loadBalance()
      } finally {
        this.mining = false
      }
    }
  }
}
</script>

<style scoped>
.page-section {
  margin-bottom: 24px;
}
.page-title {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 18px;
}
.empty-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 6px;
}
.wallet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
:deep(.el-descriptions__label) {
  font-size: 15px;
  font-weight: 500;
  color: #cbd5e1;
  display: inline-block !important;
  margin-right: 6px;
  min-width: 55px;
}
:deep(.el-descriptions__content) {
  display: inline !important;
  white-space: normal !important;
  line-height: 1.8;
}
.wallet-desc {
  margin-top: 8px;
  font-size: 17px;
}
.mono {
  font-family: "JetBrains Mono", monospace;
  font-size: 16px;
  color: #050510;
}
.subtext-inline {
  font-size: 12px;
  margin-left: 6px;
  color: #94a3b8;
}
.btn-row {
  margin-top: 18px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
</style>
