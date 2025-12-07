<template>
  <div class="page-section">
    <h2 class="page-title">区块链可视化</h2>

    <el-card class="app-card">
      <div class="card-body">
        <div class="toolbar">
          <div class="toolbar-left">
            <span class="section-title">区块交易数量统计</span>
            <span class="subtext">
              每个柱子代表一个区块，显示该区块中包含的交易数量（含 coinbase）。
            </span>
          </div>
          <div class="toolbar-right">
            <el-button size="small" @click="loadData" :loading="loading">
              刷新数据
            </el-button>
          </div>
        </div>

        <div ref="chartRef" class="chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
import * as echarts from "echarts"
import axios from "axios"

export default {
  data() {
    return {
      chart: null,
      loading: false
    }
  },

  methods: {
    async loadData() {
      if (!this.chart) return
      this.loading = true
      try {
        const res = await axios.get("http://127.0.0.1:5000/blocks")
        const blocks = res.data || []

        const xData = blocks.map(b => `#${b.index}`)
        const txCounts = blocks.map(b => b.transactions.length)

        const option = {
          tooltip: {
            trigger: "axis",
            formatter(params) {
              const p = params[0]
              return `
                区块高度：${p.name}<br/>
                交易数量：${p.value}
              `
            }
          },
          grid: {
            left: "4%",
            right: "4%",
            top: "10%",
            bottom: "8%",
            containLabel: true
          },
          xAxis: {
            type: "category",
            data: xData,
            axisTick: { alignWithLabel: true },
            axisLine: {
              lineStyle: { color: "#9ca3af" }
            }
          },
          yAxis: {
            type: "value",
            name: "交易数量",
            minInterval: 1,
            axisLine: {
              lineStyle: { color: "#9ca3af" }
            },
            splitLine: {
              lineStyle: { color: "rgba(148,163,184,0.25)" }
            }
          },
          series: [
            {
              name: "交易数",
              type: "bar",
              data: txCounts,
              barWidth: "55%",
              itemStyle: {
                borderRadius: [8, 8, 0, 0]
              }
            }
          ]
        }

        this.chart.setOption(option)
      } finally {
        this.loading = false
        this.chart.resize()
      }
    },

    handleResize() {
      if (this.chart) this.chart.resize()
    }
  },

  mounted() {
    this.chart = echarts.init(this.$refs.chartRef)
    this.loadData()

    window.addEventListener("resize", this.handleResize)
  },

  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  }
}
</script>

<style scoped>
.page-section {
  margin-bottom: 24px;
}

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

.chart {
  width: 100%;
  height: 380px;
  margin-top: 8px;
}
</style>
