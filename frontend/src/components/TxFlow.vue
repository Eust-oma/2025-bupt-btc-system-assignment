<template>
  <div class="flow-wrapper">

    <!-- Mempool 区域：左侧 -->
    <div class="mempool-card glass">
      <h3>Mempool（等待打包）</h3>

      <transition-group name="tx-fade" tag="div" class="tx-list">
        <div v-for="tx in mempool" :key="tx.txid" class="tx-item">
          {{ tx.txid.slice(0, 8) }}...
        </div>
      </transition-group>
    </div>

    <!-- 中间箭头 -->
    <div class="arrow-area">
      <div class="arrow" v-if="mempool.length > 0">→</div>
    </div>

    <!-- Block 区域：右侧 -->
    <div class="block-card glass">
      <h3>最新区块</h3>
      <p>{{ block.length }} 条交易</p>

      <transition-group name="tx-move" tag="div" class="tx-list">
        <div v-for="tx in block" :key="tx.txid" class="tx-item in-block">
          {{ tx.txid.slice(0, 8) }}...
        </div>
      </transition-group>
    </div>

    <!-- 底部操作按钮 -->
    <div class="actions">
      <el-button type="primary" @click="loadMempool">刷新 Mempool</el-button>
      <el-button type="success" @click="mine">挖矿（真实区块）</el-button>
      <el-button type="danger" @click="resetBlock">清空右侧</el-button>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

// 左侧 pending 交易（真实）
const mempool = ref([])

// 右侧最新区块交易（真实）
const block = ref([])

// ---------------------------
// 加载真实 Mempool（/pending）
// ---------------------------
async function loadMempool() {
  const res = await axios.get("http://127.0.0.1:5000/pending")
  mempool.value = res.data.map(tx => ({
    txid: tx.txid,
    from: tx.from,
    to: tx.to,
    amount: tx.amount
  }))
}

// ---------------------------
// 挖矿：调用后端真实 mine()
// ---------------------------
async function mine() {
  if (mempool.value.length === 0) {
    alert("当前 Mempool 为空，没有交易可打包")
    return
  }

  // 找到当前钱包作为矿工
  const list = JSON.parse(localStorage.getItem("wallets") || "[]")
  const cur = localStorage.getItem("currentWallet")
  const wallet = list.find(w => w.address === cur)

  if (!wallet) {
    alert("请先选择一个钱包作为矿工")
    return
  }

  await axios.post("http://127.0.0.1:5000/mine", {
    miner: wallet.address
  })

  // 挖矿后更新区块链数据
  await loadLatestBlock()
  await loadMempool()
}

// ---------------------------
// 加载最新区块（/blocks）
// ---------------------------
async function loadLatestBlock() {
  const res = await axios.get("http://127.0.0.1:5000/blocks")
  const chain = res.data
  const last = chain[chain.length - 1]

  const txs = last.transactions || []

  // 动画：让 tx 逐个飞入区块
  block.value = [] // 先清空右侧
  let i = 0
  const timer = setInterval(() => {
    block.value.push(txs[i])
    i++
    if (i >= txs.length) clearInterval(timer)
  }, 350)
}

// ---------------------------
// 清空右侧 Block 显示区（不影响区块链）
// ---------------------------
function resetBlock() {
  block.value = []
}

// 初始化加载
loadMempool()
loadLatestBlock()
</script>

<style scoped>
.flow-wrapper {
  width: 100%;
  height: 100%;
  padding: 40px;

  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  color: #e0e5ff;
}

/* 玻璃卡片公共样式 */
.glass {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);

  border-radius: 20px;
  padding: 24px 30px;
  min-width: 240px;

  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.mempool-card,
.block-card {
  width: 260px;
}

.tx-list {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tx-item {
  padding: 8px 14px;
  background: rgba(100, 150, 255, 0.15);
  border: 1px solid rgba(150, 180, 255, 0.3);
  border-radius: 10px;
  font-size: 14px;
  color: #d0d8ff;

  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* 箭头区域 */
.arrow-area {
  flex: 1;
  display: flex;
  justify-content: center;
  padding-top: 80px;
}

.arrow {
  font-size: 48px;
  color: #889cff;
  animation: arrow-blink 1.4s infinite;
}

@keyframes arrow-blink {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}

/* 按钮区域 */
.actions {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}

/* ===================== 关键：过渡动画 ===================== */
:deep(.tx-fade-enter-from) {
  opacity: 0;
  transform: translateX(-30px);
}

:deep(.tx-fade-enter-active) {
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

:deep(.tx-move-enter-from) {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}

:deep(.tx-move-enter-active) {
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
</style>
