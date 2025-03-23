# 股票数据可视化与分析系统架构设计

## 1. 系统概述

本文档提供了基于现有股票和指数数据库构建一个完整的数据可视化与分析系统的架构设计。该系统将展示数据库中的股票和指数数据，支持K线图展示，并提供选股策略运行功能。

## 2. 系统架构

### 2.1 整体架构

系统采用前后端分离的架构设计：

```
+------------------+    +------------------+    +------------------+
|                  |    |                  |    |                  |
|  前端应用层       |<-->|  后端服务层      |<-->|  数据存储层      |
|  (React + Vite)  |    |  (FastAPI)      |    |  (PostgreSQL)   |
|                  |    |                  |    |                  |
+------------------+    +------------------+    +------------------+
                              |
                              v
                        +------------------+
                        |                  |
                        |  策略分析层      |
                        |  (Python)       |
                        |                  |
                        +------------------+
```

### 2.2 各层功能

#### 2.2.1 前端应用层

- **技术栈**：React + Vite + Ant Design + ECharts
- **主要功能**：
  - 股票和指数数据展示（表格、K线图、分时图等）
  - 用户交互界面（查询、筛选、对比等）
  - 选股策略配置和结果展示
  - 数据分析报表和可视化图表

#### 2.2.2 后端服务层

- **技术栈**：FastAPI + SQLAlchemy
- **主要功能**：
  - RESTful API接口提供数据访问
  - 数据处理和转换
  - 选股策略执行
  - 用户认证和授权

#### 2.2.3 数据存储层

- **技术栈**：PostgreSQL
- **主要功能**：
  - 存储股票和指数历史数据
  - 存储选股策略和结果
  - 存储用户配置和偏好

#### 2.2.4 策略分析层

- **技术栈**：Python + pandas + numpy + TA-Lib
- **主要功能**：
  - 实现各种选股策略
  - 技术指标计算
  - 回测框架
  - 策略性能评估

## 3. 详细设计

### 3.1 前端设计

#### 3.1.1 页面结构

1. **首页**：系统概览，显示主要指数走势、热门股票、最新市场动态
2. **股票页面**：
   - 股票列表（可筛选、排序）
   - 单只股票详情（基本信息、K线图、技术指标、财务数据）
   - 多股票对比功能
3. **指数页面**：
   - 指数列表（可筛选、排序）
   - 单个指数详情（K线图、成分股、行业分布）
   - 多指数对比功能
4. **选股策略页面**：
   - 策略列表和说明
   - 策略参数配置
   - 策略运行结果展示
   - 策略回测和评估
5. **数据分析页面**：
   - 市场热度分析
   - 行业板块分析
   - 技术指标分析
   - 自定义分析报表

#### 3.1.2 K线图组件设计

使用ECharts实现专业的K线图展示：

- 支持多种时间周期（日K、周K、月K等）
- 支持多种技术指标叠加（MA、MACD、KDJ、RSI等）
- 支持缩放、拖动、十字光标等交互功能
- 支持绘制趋势线、支撑/阻力位等自定义标记

#### 3.1.3 数据请求和状态管理

- 使用React Query进行数据请求和缓存
- 使用Context API或Redux进行全局状态管理
- 实现数据预加载和懒加载策略，优化性能

### 3.2 后端API设计

#### 3.2.1 股票数据API

```
GET /api/v1/stocks                  # 获取股票列表
GET /api/v1/stocks/{symbol}         # 获取单只股票基本信息
GET /api/v1/stocks/{symbol}/kline   # 获取股票K线数据
GET /api/v1/stocks/{symbol}/indicators # 获取股票技术指标
```

#### 3.2.2 指数数据API

```
GET /api/v1/indices                 # 获取指数列表
GET /api/v1/indices/{symbol}        # 获取单个指数基本信息
GET /api/v1/indices/{symbol}/kline  # 获取指数K线数据
GET /api/v1/indices/{symbol}/components # 获取指数成分股
```

#### 3.2.3 选股策略API

```
GET /api/v1/strategies              # 获取可用策略列表
GET /api/v1/strategies/{id}         # 获取策略详情
POST /api/v1/strategies/{id}/run    # 运行选股策略
GET /api/v1/strategies/results/{id} # 获取策略运行结果
```

### 3.3 选股策略设计

#### 3.3.1 策略框架

创建一个灵活的策略框架，支持多种选股策略：

```python
class BaseStrategy:
    """基础策略类"""
    def __init__(self, params=None):
        self.params = params or {}
        
    def run(self, data):
        """运行策略"""
        raise NotImplementedError
        
    def evaluate(self, results):
        """评估策略结果"""
        raise NotImplementedError
```

#### 3.3.2 示例策略

1. **均线突破策略**：
   - 当短期均线上穿长期均线时产生买入信号
   - 当短期均线下穿长期均线时产生卖出信号

2. **MACD策略**：
   - 当MACD柱由负转正时产生买入信号
   - 当MACD柱由正转负时产生卖出信号

3. **量价关系策略**：
   - 价格上涨且成交量增加时产生买入信号
   - 价格下跌且成交量增加时产生卖出信号

4. **基本面筛选策略**：
   - 根据PE、PB、ROE等基本面指标筛选股票

### 3.4 数据更新机制

#### 3.4.1 定时任务

利用现有的定时任务机制，每天自动更新股票和指数数据：

```python
def run_scheduled_tasks():
    """定期运行数据下载任务"""
    while True:
        logger.info("开始执行定时数据下载任务...")
        download_all_stock_data()
        download_all_index_data()
        logger.info("定时数据下载任务执行完成，等待下次执行...")
        time.sleep(86400)  # 每天执行一次
```

#### 3.4.2 实时数据更新（可选）

对于需要实时数据的场景，可以考虑接入实时行情API：

- 使用WebSocket建立实时数据连接
- 实现行情推送和自动更新机制

## 4. 技术实现建议

### 4.1 前端实现

1. **项目初始化**：
   ```bash
   npm create vite@latest stock-insight-frontend -- --template react-ts
   cd stock-insight-frontend
   npm install
   ```

2. **安装必要依赖**：
   ```bash
   npm install antd @ant-design/icons @ant-design/pro-components
   npm install echarts echarts-for-react
   npm install axios react-query
   npm install react-router-dom
   ```

3. **目录结构**：
   ```
   src/
   ├── assets/         # 静态资源
   ├── components/     # 通用组件
   │   ├── KLineChart/  # K线图组件
   │   ├── DataTable/   # 数据表格组件
   │   └── ...
   ├── pages/          # 页面组件
   │   ├── Home/
   │   ├── Stock/
   │   ├── Index/
   │   ├── Strategy/
   │   └── ...
   ├── services/       # API服务
   ├── utils/          # 工具函数
   ├── hooks/          # 自定义Hooks
   ├── contexts/       # 上下文
   ├── App.tsx
   └── main.tsx
   ```

### 4.2 后端扩展

基于现有的FastAPI后端，需要扩展以下功能：

1. **扩展API端点**：
   - 添加获取股票列表、K线数据的API
   - 添加选股策略相关API
   - 添加技术指标计算API

2. **实现技术指标计算**：
   - 使用TA-Lib库计算常用技术指标
   - 缓存计算结果以提高性能

3. **实现选股策略框架**：
   - 创建策略基类和具体策略实现
   - 提供策略参数配置和结果存储机制

### 4.3 数据库扩展

需要扩展现有数据库模型，添加以下表：

1. **技术指标表**：存储预计算的技术指标
   ```
   CREATE TABLE technical_indicators (
       symbol VARCHAR(20) NOT NULL,
       date DATE NOT NULL,
       ma5 FLOAT,
       ma10 FLOAT,
       ma20 FLOAT,
       ma30 FLOAT,
       ma60 FLOAT,
       ma120 FLOAT,
       ma250 FLOAT,
       ema12 FLOAT,
       ema26 FLOAT,
       dif FLOAT,
       dea FLOAT,
       macd FLOAT,
       k FLOAT,
       d FLOAT,
       j FLOAT,
       rsi6 FLOAT,
       rsi12 FLOAT,
       rsi24 FLOAT,
       PRIMARY KEY (symbol, date)
   );
   ```
2. **策略表**：存储策略定义和参数
3. **策略结果表**：存储策略运行结果
4. **用户表**（可选）：存储用户信息和偏好设置

## 5. 部署方案

### 5.1 开发环境

1. **前端**：
   ```bash
   cd stock-insight-frontend
   npm run dev
   ```

2. **后端**：
   ```bash
   cd stock-insight
   python src/main.py
   ```

### 5.2 生产环境

1. **Docker部署**：
   - 前端和后端分别构建Docker镜像
   - 使用Docker Compose编排服务

2. **Kubernetes部署**（可扩展现有K8s配置）：
   - 部署前端、后端和数据库服务
   - 配置服务发现和负载均衡
   - 设置自动扩缩容

## 6. 后续扩展方向

1. **用户系统**：添加用户注册、登录和权限管理
2. **个性化推荐**：基于用户行为和偏好推荐股票和策略
3. **社区功能**：用户可以分享和讨论选股策略
4. **机器学习模型**：引入机器学习模型进行股价预测
5. **移动端应用**：开发配套的移动端应用

## 7. 实施路线图

### 第一阶段：基础功能实现（1-2周）

- 搭建前端项目框架
- 实现股票和指数数据展示
- 实现基本K线图组件

### 第二阶段：高级功能开发（2-3周）

- 实现选股策略框架和示例策略
- 增强K线图功能，添加技术指标
- 实现数据分析和报表功能

### 第三阶段：系统优化和部署（1-2周）

- 性能优化和代码重构
- 编写测试用例和文档
- 部署到生产环境

## 8. 总结

本文档提供了一个完整的股票数据可视化与分析系统的架构设计，包括前后端架构、数据可视化方案、选股策略实现以及系统部署建议。通过实施这一设计，可以构建一个功能丰富、性能优良的股票分析平台，满足用户对股票和指数数据展示、K线图分析以及选股策略运行的需求。