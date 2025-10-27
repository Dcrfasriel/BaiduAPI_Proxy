# BaiduAPI_Proxy
百度API转接服务

## 项目简介 (Project Introduction)

BaiduAPI_Proxy 是一个百度API转接服务，用于代理转发请求到百度的各种API服务（如翻译API、自然语言处理API等）。该服务提供了统一的接口来访问百度的API服务。

BaiduAPI_Proxy is a Baidu API proxy service that forwards requests to various Baidu API services (such as Translation API, NLP API, etc.). It provides a unified interface to access Baidu's API services.

## 功能特性 (Features)

- ✅ 百度翻译API代理 (Baidu Translation API Proxy)
- ✅ 百度自然语言处理API代理 (Baidu NLP API Proxy)
- ✅ 请求转发与身份验证 (Request forwarding with authentication)
- ✅ 错误处理和日志记录 (Error handling and logging)
- ✅ RESTful API接口 (RESTful API endpoints)

## 安装部署 (Installation)

### 环境要求 (Requirements)

- Python 3.7+
- pip

### 安装步骤 (Installation Steps)

1. 克隆项目 (Clone the repository):
```bash
git clone https://github.com/Dcrfasriel/BaiduAPI_Proxy.git
cd BaiduAPI_Proxy
```

2. 安装依赖 (Install dependencies):
```bash
pip install -r requirements.txt
```

3. 配置API密钥 (Configure API keys):
```bash
cp config.example.json config.json
```

编辑 `config.json` 文件，填入你的百度API密钥：
```json
{
  "baidu": {
    "app_id": "your_app_id_here",
    "api_key": "your_api_key_here",
    "secret_key": "your_secret_key_here"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  }
}
```

4. 运行服务 (Run the service):
```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API接口文档 (API Documentation)

### 1. 健康检查 (Health Check)

**端点 (Endpoint):** `GET /health`

**响应示例 (Response Example):**
```json
{
  "status": "healthy",
  "service": "baidu-api-proxy"
}
```

### 2. 翻译服务 (Translation Service)

**端点 (Endpoint):** `POST /api/translate`

**请求体 (Request Body):**
```json
{
  "query": "Hello, world!",
  "from": "en",
  "to": "zh"
}
```

**参数说明 (Parameters):**
- `query`: 要翻译的文本 (Text to translate)
- `from`: 源语言代码 (Source language code, e.g., "en", "zh", "auto")
- `to`: 目标语言代码 (Target language code)

**响应示例 (Response Example):**
```json
{
  "from": "en",
  "to": "zh",
  "trans_result": [
    {
      "src": "Hello, world!",
      "dst": "你好，世界！"
    }
  ]
}
```

### 3. 情感分析服务 (Sentiment Analysis Service)

**端点 (Endpoint):** `POST /api/nlp/sentiment`

**请求体 (Request Body):**
```json
{
  "text": "这个产品非常好用！"
}
```

**参数说明 (Parameters):**
- `text`: 要分析的文本 (Text to analyze)

**响应示例 (Response Example):**
```json
{
  "text": "这个产品非常好用！",
  "items": [
    {
      "positive_prob": 0.95,
      "confidence": 0.92,
      "negative_prob": 0.05,
      "sentiment": 2
    }
  ]
}
```

## 使用示例 (Usage Examples)

### 使用curl进行翻译 (Translation with curl):
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, world!",
    "from": "en",
    "to": "zh"
  }'
```

### 使用Python请求 (Python request):
```python
import requests

url = "http://localhost:5000/api/translate"
data = {
    "query": "Hello, world!",
    "from": "en",
    "to": "zh"
}

response = requests.post(url, json=data)
print(response.json())
```

## 获取百度API密钥 (Getting Baidu API Keys)

1. 访问百度翻译开放平台：https://fanyi-api.baidu.com/
2. 注册账号并创建应用
3. 获取 APP ID 和密钥
4. 访问百度AI开放平台：https://ai.baidu.com/
5. 创建应用并获取 API Key 和 Secret Key

## 注意事项 (Notes)

- 请勿将包含真实密钥的 `config.json` 文件提交到版本控制系统
- 建议在生产环境中使用环境变量来管理敏感信息
- 百度API有调用频率限制，请查看官方文档了解详情

## 许可证 (License)

MIT License

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

Welcome to submit Issues and Pull Requests!
