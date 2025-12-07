import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入 ECharts（如果有图表组件）
import * as echarts from 'echarts'

// 创建应用
const app = createApp(App)

// 全局挂载 Element Plus
app.use(ElementPlus)

// 将 echarts 加到全局，方便组件里使用 this.$echarts
app.config.globalProperties.$echarts = echarts

// 挂载到页面
app.mount('#app')
