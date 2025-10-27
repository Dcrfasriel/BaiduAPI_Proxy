# 百度搜索转接服务

## 功能说明

这是一个本地服务转接程序，用于接收GET请求并转发搜索请求到百度AI搜索服务。

### 主要功能

1. **接收GET请求**：接收包含`search`和`key`参数的GET请求
2. **密钥验证**：验证请求中的`key`参数是否与`key.txt`文件中的内容一致
3. **转发请求**：验证通过后，将搜索内容以POST请求发送到百度AI搜索服务
4. **返回结果**：将百度服务器的响应结果返回给请求者

## 安装依赖

首先需要安装Python依赖包：

```bash
pip install flask requests
```

## 使用方法

### 1. 启动服务

```bash
python search_proxy.py
```

服务将在 `http://localhost:5000` 启动

### 2. 发送搜索请求

**请求格式：**
```
GET http://localhost:5000/search?search=<搜索内容>&key=<密钥>
```

**示例：**
```bash
# 使用curl
curl "http://localhost:5000/search?search=北京有哪些旅游景区&key=12345"

# 使用浏览器
http://localhost:5000/search?search=北京有哪些旅游景区&key=12345
```

### 3. API端点

#### 搜索接口
- **URL**: `/search`
- **方法**: `GET`
- **参数**:
  - `search` (必需): 搜索内容
  - `key` (必需): 验证密钥

**成功响应 (200)**:
```json
{
  "success": true,
  "search_query": "北京有哪些旅游景区",
  "baidu_response": {
    "status_code": 200,
    "headers": {...},
    "content": {...}
  }
}
```

**失败响应**:
- 400: 缺少必需参数
- 403: 密钥验证失败
- 500: 服务器错误

#### 首页
- **URL**: `/`
- **方法**: `GET`
- **说明**: 返回服务信息

#### 健康检查
- **URL**: `/health`
- **方法**: `GET`
- **说明**: 检查服务状态

## 配置说明

### 密钥文件 (key.txt)
程序会读取与脚本同目录下的`key.txt`文件作为验证密钥。
当前密钥内容为：`12345`

### 百度API配置
程序中已配置百度AI搜索服务的API地址和Token：
- **API URL**: `https://qianfan.baidubce.com/v2/ai_search/chat/completions`
- **Token**: 已在代码中配置

## 注意事项

1. **密钥安全**：请妥善保管`key.txt`文件，避免泄露
2. **API限制**：百度API可能有调用频率限制，请合理使用
3. **网络要求**：需要能够访问百度服务器的网络环境
4. **端口占用**：确保5000端口未被其他程序占用

## 错误处理

程序会处理以下错误情况：
- 参数缺失
- 密钥验证失败
- 网络请求超时
- 百度API返回错误

所有错误都会以JSON格式返回，包含错误信息和状态码。

## 开发信息

- **Python版本**: 3.6+
- **依赖包**: Flask, Requests
- **开发模式**: 默认启用Debug模式，生产环境请关闭

## 示例测试

启动服务后，可以使用以下命令进行测试：

```bash
# 正确的请求
curl "http://localhost:5000/search?search=天气&key=12345"

# 密钥错误
curl "http://localhost:5000/search?search=天气&key=wrong"

# 缺少参数
curl "http://localhost:5000/search?key=12345"
```
