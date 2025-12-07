# BTC System —— 基于 Flask + Vue3 的区块链系统

本项目实现了一个具有真实挖矿难度验证（PoW）、交易签名、UTXO 模型、Mempool、区块浏览器、钱包系统、动态图表与可视化界面的 **完整迷你区块链系统**。
 后端使用 **Python Flask** + 自实现区块链核心逻辑，前端基于 **Vue3 + Element Plus + ECharts** 打造完整交互界面。

本仓库适合作为课程作业、区块链原理教学演示、入门项目或个人学习使用。

------

# 功能总览

### 钱包系统

- 使用 ECDSA（secp256k1）生成私钥、公钥、钱包地址
- 支持导入钱包
- 本地浏览器保存钱包列表
- 钱包余额实时查询（UTXO 模型）

### 交易系统

- UTXO 模型
- 支持发送交易
- 私钥自动签名
- 验证签名的合法性
- Mempool 待打包交易池

### 挖矿（PoW）

- SHA256 + 难度前导零要求
- Coinbase 奖励
- 打包 pending 交易
- 自动更新 UTXO 集合

### 区块链系统

- 交易列表
- 区块头信息（Hash、PrevHash、Nonce、难度、时间戳）
- 美观的区块链时间线（BlockList.vue）
- 动态区块飞入动画（ChainAnimation.vue）

### 图表可视化（ECharts）

- 每个区块的交易数量柱状图
- 动态响应式布局

### 实时交易流动动画

- 从 Mempool → Block 的动态流转
- 真实与可视化结合

------

# 项目结构

```
btc-system/
│
├── backend/
│   ├── api.py            # Flask 主接口（交易、挖矿、钱包、链）
│   ├── main.py           # 早期入口（现已整合）
│   ├── wallet/
│   │   └── wallet.py     # ECDSA 钱包、签名、验证
│   └── blockchain/
│       ├── block.py      # 区块结构
│       ├── transaction.py# 交易结构（输入/输出/签名）
│       ├── utxo.py       # UTXO 模型
│       └── blockchain.py # 核心区块链逻辑
│
├── frontend/
│   ├── App.vue           # 根组件 + 导航
│   ├── main.js           # Vue 启动入口
│   ├── style.css         # 全局样式（星空主题）
│   └── components/
│       ├── WalletView.vue
│       ├── SendTransaction.vue
│       ├── BlockList.vue
│       ├── PendingView.vue
│       ├── ChainChart.vue
│       ├── ChainAnimation.vue
│       ├── TxFlow.vue
│       └── WalletManager.vue
```

------

# 技术栈说明

### 后端 Backend

- **Python 3.10**
- **Flask**
- **ecdsa 库**（签名）
- **hashlib**（SHA256）
- 自实现：
  - 区块结构
  - 交易结构
  - 签名验证
  - Mempool
  - UTXO 管理
  - 挖矿（PoW）

### 前端 Frontend

- **Vue3（Composition API）**
- **Element Plus**
- **Axios**
- **ECharts**
- 自定义动画（CSS + transition-group）

------

# 快速启动

## 后端启动（Flask）

```
cd backend
pip install -r requirements.txt
python api.py
```

成功后会启动：

```
http://127.0.0.1:5000
```

------

## 前端启动（Vue）

```
cd frontend
npm install
npm run dev
```

浏览器访问：

```
http://localhost:5173
```

------

# 关键流程说明（Mermaid 流程图）

## 交易发送流程（横向）

```
flowchart LR
    A[用户输入交易信息] --> B[使用私钥签名交易]
    B --> C[提交到后端 /tx/create_signed]
    C --> D[Mempool 等待打包]
    D --> E[矿工挖矿 /mine]
    E --> F[生成新区块]
    F --> G[更新 UTXO 集]
    G --> H[前端刷新显示]
```

## 挖矿流程（横向）

```
flowchart LR
    A[获取 pending 交易] --> B[构造区块]
    B --> C[执行 PoW 寻找 nonce]
    C --> D[成功找到满足难度的哈希]
    D --> E[写入区块链]
    E --> F[coinbase 奖励给矿工]
```

------

# API 文档（简版）

## 获取链

```
GET /blocks
```

## 创建交易

```
POST /transaction
{
  "sender": "...",
  "receiver": "...",
  "amount": 10,
  "signature": "..."
}
```

## 挖矿

```
POST /mine
{ "miner": "address" }
```

## 创建钱包

```
GET /create_wallet
```

## 查询余额

```
GET /balance/<address>
```

## 获取 Mempool

```
GET /pending
```

## 自动生成签名交易

```
POST /tx/create_signed
```
