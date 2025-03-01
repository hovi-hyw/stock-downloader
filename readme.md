# Stock Data Service

## 项目简介

本项目是一个用于下载和存储股票、指数、概念板块数据的服务。

## 功能

*   下载股票日线数据
*   下载指数日线数据
*   存储数据到 PostgreSQL 数据库
*   提供 API 接口访问数据

## 快速开始

1.  **克隆代码:**

    ```bash
    git clone <repository_url>
    cd stock-data-service
    ```

2.  **配置环境变量:**

    创建 `.env` 文件，并配置以下环境变量：

    ```
    DATABASE_URL=postgresql://si:jojo@localhost:5432/stock
    MAX_WORKERS=4
    BATCH_SIZE=100
    API_RETRY_COUNT=3
    API_RETRY_DELAY=1

    LOG_LEVEL=INFO

    # 列表更新频率
    MAX_CSV_AGE_DAYS=100
    # CSV 文件路径
    CACHE_PATH=cache

    MAX_RETRIES=3
    RETRY_DELAY=5
    GET_TIMEOUT=10
    MAX_THREADS=12
    ```

3.  **构建 Docker 镜像:**

    ```bash
    docker build -t your-docker-repo/stock-data-service:latest .
    ```

4.  **运行 Docker Compose (可选):**

    ```bash
    docker-compose up -d
    ```

5.  **部署到 Kubernetes:**

    *   确保您已安装 `kubectl` 并配置为连接到您的 Kubernetes 集群。
    *   替换 `k8s/deployment.yaml` 和 `k8s/service.yaml` 中的占位符（例如，`your-docker-repo/stock-data-service:latest` 和 `postgresql://si:jojo@your-postgres-service:5432/stock`）为您的实际值。
    *   如果您使用 Ingress，请配置 `k8s/ingress.yaml` 并确保您的 Ingress Controller 正在运行。

    ```bash
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    kubectl apply -f k8s/ingress.yaml  # 如果您使用 Ingress
    ```

## 使用

### API 接口

*   `GET /api/v1/stock/{symbol}/{date}`: 获取指定股票指定日期的日线数据
*   `GET /api/v1/index/{symbol}/{date}`: 获取指定指数指定日期的日线数据

### 健康检查

*   您可以添加健康检查探针（livenessProbe 和 readinessProbe）到 `k8s/deployment.yaml` 中。
*   您需要在 FastAPI 应用中定义一个 `/health` 端点，用于返回健康状态。

## 贡献

欢迎提交 issue 和 pull request!