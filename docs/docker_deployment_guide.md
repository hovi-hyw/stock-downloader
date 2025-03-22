# Docker 部署指南

本文档提供了使用 Docker 部署股票数据服务的详细指南，包括股票列表下载服务的独立部署。

## 目录

- [环境准备](#环境准备)
- [项目结构](#项目结构)
- [服务说明](#服务说明)
- [部署步骤](#部署步骤)
- [服务管理](#服务管理)
- [数据持久化](#数据持久化)
- [常见问题](#常见问题)

## 环境准备

在开始部署之前，请确保您的系统已安装以下软件：

1. **Docker**：版本 20.10.0 或更高
   - 安装指南：[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

2. **Docker Compose**：版本 2.0.0 或更高
   - 安装指南：[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## 项目结构

本项目包含以下主要组件：

- **主应用服务**：提供 API 接口和数据下载功能
- **股票列表下载服务**：独立的服务，专门负责在交易日的特定时间（9:26）自动下载早盘集合竞价的股票列表
- **PostgreSQL 数据库**：存储股票和指数数据

## 服务说明

### 主应用服务

主应用服务提供以下功能：

- RESTful API 接口，用于查询股票和指数数据
- 定期下载股票和指数的日线数据
- 数据处理和存储

### 股票列表下载服务

股票列表下载服务是一个独立的服务，具有以下特点：

- 在每个交易日的上午 9:26 自动下载早盘集合竞价的股票列表
- 将股票列表保存为带有日期时间的文件，便于追踪历史变化
- 同时更新标准位置的股票列表文件，供主应用服务使用

## 部署步骤

### 1. 获取项目代码

```bash
git clone <repository_url>
cd stock-downloader
```

### 2. 配置环境变量（可选）

项目已在 `docker-compose.yml` 中配置了默认的环境变量。如果需要自定义，可以修改该文件中的环境变量配置。

### 3. 构建并启动服务

```bash
docker-compose up -d
```

此命令将：
- 构建主应用服务和股票列表下载服务的 Docker 镜像
- 创建并启动 PostgreSQL 数据库容器
- 创建并启动主应用服务容器
- 创建并启动股票列表下载服务容器

### 4. 验证服务状态

```bash
docker-compose ps
```

确认所有服务都处于 `Up` 状态。

## 服务管理

### 查看服务日志

查看主应用服务日志：

```bash
docker-compose logs -f stock-data-service
```

查看股票列表下载服务日志：

```bash
docker-compose logs -f stock-list-service
```

### 重启服务

重启所有服务：

```bash
docker-compose restart
```

重启特定服务：

```bash
docker-compose restart stock-list-service
```

### 停止服务

停止所有服务：

```bash
docker-compose down
```

## 数据持久化

本项目使用 Docker 卷和主机目录挂载来实现数据持久化：

- **数据库数据**：存储在名为 `postgres_data` 的 Docker 卷中
- **缓存文件**：挂载到主机的 `./cache` 目录
- **日志文件**：挂载到主机的 `./logs` 目录

这确保了即使容器被删除，数据也不会丢失。

## 常见问题

### 1. 服务无法连接到数据库

**问题**：服务启动后报告无法连接到数据库。

**解决方案**：
- 确认 PostgreSQL 容器已正常启动：`docker-compose ps postgres`
- 检查数据库连接配置：确保 `docker-compose.yml` 中的 `DATABASE_URL` 环境变量正确
- 尝试重启服务：`docker-compose restart`

### 2. 股票列表下载服务没有在预期时间执行

**问题**：在交易日的 9:26 没有看到股票列表下载的日志。

**解决方案**：
- 检查服务日志：`docker-compose logs -f stock-list-service`
- 确认系统时间是否正确：`docker exec stock-list-service date`
- 手动触发下载（用于测试）：
  ```bash
  docker exec -it stock-list-service python -c "from StockDownloader.src.services.stock_list_service import download_stock_list_task; download_stock_list_task()"
  ```

### 3. 容器启动失败

**问题**：容器无法启动或立即退出。

**解决方案**：
- 查看容器日志：`docker-compose logs <service_name>`
- 检查 Docker 镜像构建是否成功：`docker-compose build --no-cache <service_name>`
- 确认项目文件权限正确

### 4. 数据卷权限问题

**问题**：服务无法写入挂载的目录。

**解决方案**：
- 确保主机上的 `cache` 和 `logs` 目录存在且具有正确的权限
- 手动创建目录并设置权限：
  ```bash
  mkdir -p cache logs
  chmod 777 cache logs
  ```

### 5. 如何更新服务

**问题**：如何更新服务到最新版本。

**解决方案**：
1. 获取最新代码：`git pull`
2. 重新构建镜像：`docker-compose build --no-cache`
3. 重启服务：`docker-compose up -d`