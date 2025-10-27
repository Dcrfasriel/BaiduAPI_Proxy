# 百度搜索转接服务

这是一个本地服务转接程序，用于接收GET请求并转发搜索请求到百度AI搜索服务。

## 功能特点

- ✅ 接收GET请求（包含search和key参数）
- ✅ 密钥验证（与key.txt文件内容比对）
- ✅ 转发到百度AI搜索API
- ✅ 返回格式化的问答结果 `[{q:'问题',a:'回答'}]`

## 部署指南

### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动服务：
```bash
python search_proxy.py
```

3. 访问服务：
```
http://localhost:5000/search?search=<搜索内容>&key=<密钥>
```

### 部署到云平台

#### 方式1: Render.com (推荐)

1. Fork或上传此项目到GitHub
2. 注册 [Render.com](https://render.com)
3. 创建新的Web Service
4. 连接您的GitHub仓库
5. 配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python search_proxy.py`
   - **Port**: `5000`
6. 部署完成！

#### 方式2: Railway.app

1. 注册 [Railway.app](https://railway.app)
2. 从GitHub导入项目
3. Railway会自动检测Procfile并部署
4. 获取分配的URL

#### 方式3: Heroku

1. 安装Heroku CLI
2. 登录Heroku：
```bash
heroku login
```

3. 创建应用：
```bash
heroku create your-app-name
```

4. 部署：
```bash
git push heroku main
```

### 环境变量配置

对于生产环境，建议将敏感信息设置为环境变量：

- `BAIDU_API_TOKEN`: 百度API令牌
- `SECRET_KEY`: 验证密钥（替代key.txt）

## API文档

### 搜索接口

**端点**: `/search`  
**方法**: `GET`  
**参数**:
- `search` (必需): 搜索内容
- `key` (必需): 验证密钥

**响应格式**:
```json
[
  {
    "q": "问题",
    "a": "回答内容"
  }
]
```

### 其他接口

- `/` - 服务信息
- `/health` - 健康检查

## 注意事项

⚠️ **GitHub Pages限制**: GitHub Pages只能托管静态网站，不支持Flask等后端服务。请使用上述云平台进行部署。

## 技术栈

- Python 3.13
- Flask 2.3.3
- Requests 2.31.0

## 许可证

MIT License
