<template>
  <el-dialog
    :model-value="show"
    @update:model-value="(v) => emit('update:show', v)"
    width="600px"
    title="钱包列表管理"
  >
    <div class="wallet-list">
      <h3>钱包列表</h3>

      <el-empty v-if="wallets.length === 0" description="暂无钱包" />

      <div
        v-for="(w, index) in wallets"
        :key="index"
        class="wallet-item"
        @click="useWallet(index)"
      >
        <div class="addr">
          <div class="name">{{ w.name || `钱包 ${index + 1}` }}</div>
          <div class="address">{{ w.address }}</div>
        </div>
        <div class="btns">
          <el-button type="primary" @click.stop="useWallet(index)">使用</el-button>
          <el-button type="danger" @click.stop="deleteWallet(index)">删除</el-button>
        </div>
      </div>

      <el-divider />

      <el-button type="success" @click="createWallet">
        创建新钱包
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from "vue"

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(["update:show", "changed"])

const wallets = ref([])

function loadWallets() {
  wallets.value = JSON.parse(localStorage.getItem("wallets") || "[]")
}

function saveWallets() {
  localStorage.setItem("wallets", JSON.stringify(wallets.value))
}

async function createWallet() {
  // 调用后端真实钱包生成接口
  const res = await fetch("http://127.0.0.1:5000/create_wallet");
  const newWallet = await res.json();

  // 自动添加名称
  newWallet.name = `钱包 ${wallets.value.length + 1}`;

  // 保存到本地钱包列表
  wallets.value.push(newWallet);
  saveWallets();

  // 设置为当前钱包
  localStorage.setItem("currentWallet", newWallet.address);
  emit("changed", newWallet);
}


function useWallet(index) {
  const w = wallets.value[index]
  if (!w) return
  localStorage.setItem("currentWallet", w.address)
  emit("changed", w)
}

function deleteWallet(index) {
  wallets.value.splice(index, 1)
  saveWallets()
}

onMounted(loadWallets)
</script>

<style scoped>
.wallet-item {
  background: #1f1f1f;
  color: white;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}
.addr {
  font-size: 14px;
  display: flex;
  flex-direction: column;
}
.name {
  font-weight: 600;
  margin-bottom: 4px;
}
.address {
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  opacity: 0.8;
}
.btns {
  display: flex;
  gap: 8px;
}
</style>
