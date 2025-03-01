# Stock Data Service

## 项目简介

本项目是一个用于下载股票和指数数据的服务，用于构建数据库。

## 功能

*   下载股票日线数据
*   下载指数日线数据
*   存储数据到 PostgreSQL 数据库

## 快速开始

1.  **克隆代码:**

    ```bash
    git clone <repository_url>
    cd stock-data-service
    ```

2.  **配置环境变量:**

    创建 `.env` 文件，并配置以下环境变量：

    ```
    DATABASE_URL=postgresql://id:pwd@localhost:5432/db_name
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

    ```bash
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    ```

## 使用

*   运行 `src/main.py` 文件，它将下载股票和指数数据并保存到数据库。

## 贡献

欢迎提交 issue 和 pull request!