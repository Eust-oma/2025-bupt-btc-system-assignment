<template>
  <div class="page-section">
    <h2 class="page-title">Mempool（未打包交易池）</h2>

    <el-card class="app-card">
      <div class="card-body">

        <!-- 顶部工具栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <span class="section-title">交易池状态</span>
            <span class="subtext">当前共有 {{ pending.length }} 笔待确认交易</span>
          </div>

          <div class="toolbar-right">
            <el-button size="small" @click="loadPending">刷新</el-button>
          </div>
        </div>

        <!-- 空状态 -->
        <el-empty
          v-if="pending.length === 0"
          description="当前没有待处理的交易"
          style="margin-top: 30px;"
        />

        <!-- 交易列表 -->
        <el-row v-else :gutter="12">
          <el-col
            v-for="tx in pending"
            :key="tx.txid"
            :xs="24"
            :sm="12"
            :md="12"
          >
            <div class="tx-card" @click="openTx(tx)">

              <div class="tx-title">
                <span class="mono">{{ tx.txid }}</span>
              </div>

              <div class="subtext small">
                输入：{{ tx.inputs.length }} ｜ 输出：{{ tx.outputs.length }}
              </div>
            </div>
          </el-col>
        </el-row>

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

        <h4 style="margin-top: 20px;">Inputs（输入）</h4>
        <el-empty
          v-if="currentTx.inputs.length === 0"
          description="Coinbase 交易，无输入"
        />
        <ul v-else class="list">
          <li v-for="i in currentTx.inputs" :key="i.txid + '-' + i.index">
            来源 Tx：<span class="mono small">{{ i.txid }}</span>
            ｜ 输出序号：{{ i.index }}
          </li>
        </ul>

        <h4 style="margin-top: 20px;">Outputs（输出）</h4>
        <ul class="list">
          <li v-for="(o, idx) in currentTx.outputs" :key="o.address + '-' + idx">
            序号 {{ idx }} ｜ 地址：
            <span class="mono small">{{ o.address }}</span>
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
      pending: [],
      showTx: false,
      currentTx: null
    }
  },

  methods: {
    /** 加载 pending transactions */
    async loadPending() {
      const res = await axios.get("http://127.0.0.1:5000/pending")
      this.pending = res.data
    },

    /** 打开交易详情弹窗 */
    openTx(tx) {
      this.currentTx = tx
      this.showTx = true
    }
  },

  mounted() {
    this.loadPending()
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
}

/* 交易卡片 */
.tx-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 12px;
  background: rgba(15, 23, 42, 0.03);
  cursor: pointer;
  transition: 0.2s;
}
.tx-card:hover {
  background: var(--accent-soft);
}

.tx-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

/* 列表样式 */
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
</style>
