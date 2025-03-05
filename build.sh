# 创建前端项目结构
mkdir -p stock-insight-frontend/src/{assets,components,pages,services,utils,hooks,contexts}
mkdir -p stock-insight-frontend/src/components/{KLineChart,DataTable}
mkdir -p stock-insight-frontend/src/pages/{Home,Stock,Index,Strategy}
touch stock-insight-frontend/src/App.tsx
touch stock-insight-frontend/src/main.tsx
touch stock-insight-frontend/package.json
touch stock-insight-frontend/.gitignore

# 创建后端项目结构
mkdir -p stock-insight-backend/{src,tests,docs}
mkdir -p stock-insight-backend/src/{api,core,database,services,tasks,utils}
mkdir -p stock-insight-backend/src/api/endpoints
mkdir -p stock-insight-backend/src/database/models
mkdir -p stock-insight-backend/src/services/strategies

# 创建后端基础文件
touch stock-insight-backend/src/main.py
touch stock-insight-backend/src/api/{__init__.py,app.py}
touch stock-insight-backend/src/api/endpoints/{__init__.py,stock.py,index.py,strategy.py}
touch stock-insight-backend/src/core/{__init__.py,config.py,logger.py}
touch stock-insight-backend/src/database/{__init__.py,base.py,session.py}
touch stock-insight-backend/src/services/{__init__.py,data_service.py,strategy_service.py}
touch stock-insight-backend/src/tasks/{__init__.py,scheduler.py}
touch stock-insight-backend/src/utils/{__init__.py,helpers.py}
touch stock-insight-backend/requirements.txt
touch stock-insight-backend/.env
touch stock-insight-backend/.gitignore
