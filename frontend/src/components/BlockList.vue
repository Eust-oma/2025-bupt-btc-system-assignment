<template>
  <div class="page-section">
    <h2 class="page-title">区块链浏览器</h2>

    <el-card class="app-card">
      <div class="card-body">

        <!-- 顶部工具栏 -->
        <div class="toolbar">

          <div class="toolbar-left">
            <span class="section-title">链状态</span>
            <span class="subtext">当前共有 {{ blocks.length }} 个区块</span>
          </div>

          <div class="toolbar-right">
            <el-input
              v-model="miner"
              placeholder="矿工地址（自动使用当前钱包）"
              size="small"
              clearable
              style="width: 280px;"
            />
            <el-button size="small" @click="loadBlocks">刷新</el-button>
            <el-button
              type="primary"
              size="small"
              :loading="mining"
              @click="mineBlock"
            >
              挖矿
            </el-button>
          </div>

        </div>

        <!-- 区块链时间线 -->
        <el-timeline style="margin-top: 10px;">
          <el-timeline-item
            v-for="b in blocks"
            :key="b.index"
            :timestamp="'高度 ' + b.index"
            placement="top"
          >
            <el-card class="block-card">

              <!-- 区块头 -->
              <div class="block-header">
                <div>
                  <span class="subtext">区块哈希</span>
                  <div class="mono hash">{{ b.hash }}</div>
                </div>

                <div class="block-meta">
                  <span class="subtext">前一区块</span>
                  <div class="mono small">{{ b.prev_hash }}</div>
                  <div class="subtext small">
                    难度：{{ b.difficulty }} ｜ Nonce：{{ b.nonce }} ｜ 时间戳：{{ b.timestamp }}
                  </div>
                </div>
              </div>

              <!-- 交易列表 -->
              <div class="tx-list">
                <div class="section-title">交易列表（{{ b.transactions.length }}）</div>

                <el-empty
                  v-if="b.transactions.length === 0"
                  description="此区块没有交易"
                />

                <el-row
                  v-else
                  :gutter="10"
                >
                  <el-col
                    v-for="tx in b.transactions"
                    :key="tx.txid"
                    :xs="24"
                    :sm="12"
                  >
                    <div class="tx-item" @click="openTx(tx)">
                      <div class="mono small tx-id">{{ tx.txid }}</div>
                      <div class="subtext small">
                        输入：{{ tx.inputs.length }} ｜ 输出：{{ tx.outputs.length }}
                      </div>
                    </div>
                  </el-col>
                </el-row>

              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>

      </div>
    </el-card>

    <!-- 交易详情弹窗 -->
    <el-dialog
      v-model="showTx"
      width="700px"
      title="交易详情"
    >
      <div v-if="currentTx">

        <p><strong>TxID：</strong>
          <span class="mono">{{ currentTx.txid }}</span>
        </p>
        <p><strong>时间戳：</strong>{{ currentTx.timestamp }}</p>

        <h4 style="margin-top: 20px;">Inputs（输入）</h4>
        <el-empty
          v-if="currentTx.inputs.length === 0"
          description="Coinbase 交易，无输入"
        />
        <ul v-else class="list">
          <li v-for="i in currentTx.inputs" :key="i.txid + '-' + i.index">
            来源 Tx：<span class="mono small">{{ i.txid }}</span>
            ｜ 输出序号：{{ i.index }}
            <br />
            签名：<span class="mono tiny">{{ i.signature }}</span>
          </li>
        </ul>

        <h4 style="margin-top: 20px;">Outputs（输出）</h4>
        <ul class="list">
          <li v-for="(o, idx) in currentTx.outputs" :key="o.address + '-' + idx">
            序号 {{ idx }} ｜ 地址：<span class="mono small">{{ o.address }}</span>
            ｜ 金额：{{ o.amount }} BTC
          </li>
        </ul>

      </div>

      <template #footer>
        <el-button @click="showTx = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>


<script>
import axios from "axios"

export default {
  data() {
    return {
      blocks: [],
      miner: "",
      mining: false,

      showTx: false,
      currentTx: null
    }
  },

  methods: {
    /** 加载当前钱包作为矿工地址 */
    loadCurrentWallet() {
      const wallets = JSON.parse(localStorage.getItem("wallets") || "[]")
      const current = localStorage.getItem("currentWallet")
      this.miner = wallets.find(w => w.address === current)?.address || ""
    },

    /** 加载区块链数据 */
    async loadBlocks() {
      const res = await axios.get("http://127.0.0.1:5000/blocks")
      this.blocks = res.data
    },

    /** 进行挖矿 */
    async mineBlock() {
      if (!this.miner) {
        return this.$message.warning("请先选择矿工地址（建议使用当前钱包）")
      }
      this.mining = true

      try {
        await axios.post("http://127.0.0.1:5000/mine", {
          miner: this.miner
        })
        this.$message.success("挖矿成功！新块已加入链上")
        this.loadBlocks()
      } finally {
        this.mining = false
      }
    },

    /** 打开交易详情 */
    openTx(tx) {
      this.currentTx = tx
      this.showTx = true
    }
  },

  mounted() {
    this.loadCurrentWallet()
    this.loadBlocks()
  }
}
</script>


<style scoped>
.page-section {
  margin-bottom: 24px;
}

/* 顶部工具栏 */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.toolbar-left {
  display: flex;
  flex-direction: column;
}

.toolbar-right {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 区块卡片 */
.block-card {
  margin-top: 6px;
}

/* 区块 header 布局 */
.block-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 8px;
}

/* TX Item */
.tx-item {
  border-radius: 12px;
  border: 1px solid var(--border-color);
  padding: 8px 10px;
  margin-bottom: 8px;
  background: rgba(15, 23, 42, 0.03);
  cursor: pointer;
}
.tx-item:hover {
  background: var(--accent-soft);
}

.tx-id {
  font-weight: 500;
}

/* 列表 */
.list {
  padding-left: 18px;
}

.mono {
  font-family: "JetBrains Mono", monospace;
  word-break: break-all;
}
.small {
  font-size: 12px;
}
.tiny {
  font-size: 11px;
}
.hash {
  font-size: 13px;
}
.block-meta {
  margin-top: 2px;
}

.block {
  padding: 20px;
  margin-bottom: 20px;

  background: rgba(255, 255, 255, 0.05);
  border-radius: 18px;
  backdrop-filter: blur(18px);

  border: 1px solid rgba(120, 140, 255, 0.25);

  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.25),
    0 0 12px rgba(120, 80, 255, 0.4);
}

.block p,
.block li {
  color: #e8ebff;
}
</style>
