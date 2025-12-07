<template>
  <div class="chain-canvas">
    <svg class="link-svg">
      <!-- 动态连线 -->
      <line
        v-for="(p, i) in links"
        :key="i"
        :x1="p.x1"
        :y1="p.y1"
        :x2="p.x2"
        :y2="p.y2"
        stroke="rgba(180,200,255,0.35)"
        stroke-width="2"
      />
    </svg>

    <!-- 区块节点 -->
    <div
      v-for="(b, i) in animatedBlocks"
      :key="b.hash"
      class="block-node"
      :style="{
        transform: `translate(${b.x}px, ${b.y}px)`,
        transition: b.loaded ? '1s ease' : '0s',
      }"
      @mouseenter="hover = b"
      @mouseleave="hover = null"
    >
      <div class="block-card">
        <div class="hash">{{ b.hash.slice(0, 12) }}...</div>
        <div class="index">#{{ b.index }}</div>
      </div>
    </div>

    <!-- 浮层：区块详情 -->
    <div v-if="hover" class="hover-panel">
      <p><strong>高度：</strong> {{ hover.index }}</p>
      <p><strong>Hash：</strong> {{ hover.hash }}</p>
      <p><strong>Prev：</strong> {{ hover.prev_hash }}</p>
      <p><strong>Tx：</strong> {{ hover.transactions.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const animatedBlocks = ref([])
const links = ref([])
const hover = ref(null)

// 初始化布局参数
const blockWidth = 160
const blockHeight = 80
const gap = 120

async function loadBlocks() {
  const res = await axios.get("http://127.0.0.1:5000/blocks")
  const blocks = res.data

  animatedBlocks.value = blocks.map((b, i) => ({
    ...b,
    x: -300, // 从左侧漂入
    y: 60 + i * gap,
    loaded: false
  }))

  // 让每个区块按序飞进来
  setTimeout(() => {
    animatedBlocks.value.forEach((b, i) => {
      setTimeout(() => {
        b.x = 100
        b.loaded = true
        updateLinks()
      }, i * 200)
    })
  }, 200)
}

function updateLinks() {
  links.value = animatedBlocks.value.slice(1).map((b, i) => {
    return {
      x1: 100 + blockWidth,
      y1: 60 + i * gap + blockHeight / 2,
      x2: 100,
      y2: 60 + (i + 1) * gap + blockHeight / 2,
    }
  })
}

onMounted(loadBlocks)
</script>

<style scoped>
.chain-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 600px;
}

.link-svg {
  position: absolute;
  inset: 0;
}

.block-node {
  position: absolute;
  cursor: pointer;
}

.block-card {
  width: 160px;
  height: 80px;
  padding: 12px;
  border-radius: 14px;

  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(180,200,255,0.3);

  box-shadow:
    0 4px 12px rgba(0,0,0,0.3),
    0 0 12px rgba(140,120,255,0.4);

  color: #e6e9ff;
}

.hash {
  font-size: 13px;
  opacity: 0.8;
}

.index {
  font-size: 20px;
  font-weight: bold;
}

.hover-panel {
  position: fixed;
  right: 30px;
  top: 80px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.07);
  border-radius: 12px;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(160,170,255,0.25);
  color: white;
  width: 260px;
}
</style>
