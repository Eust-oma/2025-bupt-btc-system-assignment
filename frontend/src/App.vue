<script setup>
import { ref, computed, onMounted } from "vue"

import WalletView from "./components/WalletView.vue"
import SendTransaction from "./components/SendTransaction.vue"
import BlockList from "./components/BlockList.vue"
import PendingView from "./components/PendingView.vue"
import ChainChart from "./components/ChainChart.vue"
import WalletManager from "./components/WalletManager.vue"
import TxFlow from "./components/TxFlow.vue"

const page = ref("wallet")
const showWalletManager = ref(false)

// 当前选中的钱包（完整对象）
const currentWallet = ref(null)

// 页面切换
const currentView = computed(() => {
  return {
    wallet: WalletView,
    send: SendTransaction,
    blocks: BlockList,
    pending: PendingView,
    chart: ChainChart,
    flow: TxFlow,
  }[page.value]
})

// 初始化：从 localStorage 里恢复当前钱包
onMounted(() => {
  const list = JSON.parse(localStorage.getItem("wallets") || "[]")
  const addr = localStorage.getItem("currentWallet") || ""
  currentWallet.value = list.find((w) => w.address === addr) || null
})

// 钱包被创建 / 切换时调用
function handleWalletChanged(w) {
  currentWallet.value = w
  localStorage.setItem("currentWallet", w.address)
}
</script>

<template>
  <!-- 星空粒子背景 -->
  <div id="starfield"></div>

  <el-container class="layout">
    <!-- 顶部导航栏 -->
    <el-header class="header neon-header">
      <div class="brand">
        <div class="brand-title">BTC System</div>
      </div>

      <el-menu
          mode="horizontal"
          :default-active="page"
          @select="(k) => (page = k)"
          class="nav-menu"
          background-color="transparent"
          text-color="#b8c7ff"
          active-text-color="#fff"
      >
        <el-menu-item index="wallet">钱包</el-menu-item>
        <el-menu-item index="send">发送交易</el-menu-item>
        <el-menu-item index="blocks">区块链</el-menu-item>
        <el-menu-item index="pending">Mempool</el-menu-item>
        <el-menu-item index="chart">可视化</el-menu-item>
        <el-menu-item @click="showWalletManager = true">钱包列表</el-menu-item>
        <el-menu-item index="flow">交易流动画</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 内容区域：把当前钱包传给各页面（只有 WalletView 会用到） -->
    <el-main class="main">
      <component
          :is="currentView"
          :current-wallet="currentWallet"
          @openWalletManager="showWalletManager = true"
      />
    </el-main>

    <!-- 钱包管理器：v-model 控制弹窗，@changed 更新当前钱包 -->
    <WalletManager
        v-model:show="showWalletManager"
        @changed="handleWalletChanged"
    />
  </el-container>
</template>

<style>
/* 下面这些都是你原来的样式，原封不动保留 */
#starfield {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(120, 80, 180, 0.25), transparent 70%),
  radial-gradient(circle at 70% 80%, rgba(60, 40, 150, 0.18), transparent 70%),
  linear-gradient(135deg, #030308 0%, #050510 50%, #010207 100%);
  z-index: -10;
  overflow: hidden;
}

#starfield::before,
#starfield::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("https://raw.githubusercontent.com/ghosh/uiGradients/master/gradients/stars.png");
  opacity: 0.45;
  animation: drift 120s linear infinite;
}

#starfield::after {
  opacity: 0.25;
  animation-duration: 240s;
}

@keyframes drift {
  from {
    transform: translate3d(0, 0, 0);
  }
  to {
    transform: translate3d(-800px, -1200px, 0);
  }
}

.layout {
  min-height: 100vh;
  width: 100%;
  backdrop-filter: blur(4px);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(14, 16, 32, 0.55);
  padding: 0 32px;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(90, 120, 255, 0.2);
}

.neon-header {
  box-shadow: 0 0 8px rgba(90, 120, 255, 0.5),
  0 0 16px rgba(90, 120, 255, 0.3),
  inset 0 0 6px rgba(120, 80, 255, 0.4);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-title {
  font-size: 18px;
  font-weight: 600;
  color: #dbe4ff;
}

.nav-menu {
  background: transparent !important;
  border-bottom: none !important;
}

.el-menu-item {
  transition: 0.25s;
}

.el-menu-item:hover {
  color: #fff !important;
  text-shadow: 0 0 8px #a78bfa;
}

.main {
  padding: 24px;
}

/* 折叠菜单样式保留 */
.el-menu--horizontal .el-menu--popup {
  background: rgba(20, 24, 38, 0.7) !important;
  backdrop-filter: blur(18px);
  border-radius: 14px !important;
  padding: 6px 0 !important;
  border: 1.5px solid transparent !important;
  background-clip: padding-box, border-box;
  background-image: linear-gradient(135deg, rgba(20, 24, 38, 0.7), rgba(20, 24, 38, 0.7)),
  linear-gradient(135deg, #7f5af0, #2cb7ff) !important;
  box-shadow: 0 0 12px rgba(127, 90, 240, 0.35);
}

.el-menu--horizontal .el-menu--popup .el-menu-item {
  color: #e8ecff !important;
  padding: 10px 20px !important;
  transition: 0.18s ease;
}

.el-menu--horizontal .el-menu--popup .el-menu-item:hover {
  background: rgba(127, 90, 240, 0.22) !important;
  color: white !important;
}

.el-menu--horizontal .el-menu--popup .el-menu-item.is-active {
  background: rgba(127, 90, 240, 0.35) !important;
  color: #ffffff !important;
  font-weight: 600;
}
</style>
