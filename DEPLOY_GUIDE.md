# 🚀 快速部署指南

## ⚠️ 重要说明

**GitHub Pages (github.io) 不支持Flask后端服务！**

GitHub Pages只能托管静态HTML/CSS/JS文件，无法运行Python Flask服务器。

## ✅ 推荐部署方案

### 方案1: Render.com (最简单，推荐)

**步骤：**

1. **准备GitHub仓库**
   ```powershell
   # 在项目目录执行
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 创建新仓库（不要初始化任何文件）
   - 复制仓库URL

3. **推送代码**
   ```powershell
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git branch -M main
   git push -u origin main
   ```

4. **部署到Render**
   - 访问 https://render.com
   - 点击 "Get Started" 注册（可用GitHub登录）
   - 点击 "New +" → "Web Service"
   - 连接GitHub并选择您的仓库
   - 配置：
     * **Name**: baidu-search-proxy
     * **Environment**: Python 3
     * **Build Command**: `pip install -r requirements.txt`
     * **Start Command**: `python search_proxy.py`
   - 点击 "Create Web Service"
   - 等待部署完成（约2-3分钟）
   - 获得免费的公网URL！

### 方案2: Railway.app (自动化)

1. **推送代码到GitHub**（同上）

2. **部署**
   - 访问 https://railway.app
   - 使用GitHub登录
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您的仓库
   - Railway自动检测并部署
   - 获得公网URL

### 方案3: PythonAnywhere (Python专用)

1. 注册 https://www.pythonanywhere.com
2. 上传代码或从GitHub克隆
3. 配置Web应用
4. 获得 `你的用户名.pythonanywhere.com` 域名

## 📝 使用一键部署脚本

### Windows (PowerShell)
```powershell
.\deploy.ps1
```

### Linux/Mac (Bash)
```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔧 环境变量配置（可选）

在云平台上设置环境变量（更安全）：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `BAIDU_API_TOKEN` | 百度API令牌 | `bce-v3/ALTAK-...` |
| `SECRET_KEY` | 验证密钥 | `12345` |
| `PORT` | 端口号（自动） | `5000` |
| `FLASK_ENV` | 环境模式 | `production` |

## 📊 部署平台对比

| 平台 | 免费额度 | 难度 | 速度 | 推荐度 |
|------|---------|------|------|--------|
| Render | ✅ 充足 | ⭐ 简单 | 🚀 快 | ⭐⭐⭐⭐⭐ |
| Railway | ✅ 有限 | ⭐ 简单 | 🚀 快 | ⭐⭐⭐⭐ |
| PythonAnywhere | ✅ 有限 | ⭐⭐ 中等 | 🐢 中 | ⭐⭐⭐ |
| Vercel | ⚠️ 需配置 | ⭐⭐⭐ 复杂 | 🚀 快 | ⭐⭐ |

## 🎯 部署后测试

部署完成后，使用您的公网URL测试：

```bash
# 替换 YOUR_URL 为实际部署的URL
curl "https://YOUR_URL/search?search=北京天气&key=12345"
```

或在浏览器访问：
```
https://YOUR_URL/search?search=北京天气&key=12345
```

## ❓ 常见问题

**Q: 为什么不能用GitHub Pages?**  
A: GitHub Pages只支持静态网站，不能运行Python服务器。

**Q: 免费部署有限制吗?**  
A: Render免费tier有每月750小时运行时间，足够个人项目使用。

**Q: 如何更新部署?**  
A: 直接push到GitHub，云平台会自动重新部署。

**Q: 如何查看日志?**  
A: 在Render/Railway的控制台都有日志查看功能。

## 📚 相关链接

- Render文档: https://render.com/docs
- Railway文档: https://docs.railway.app
- Flask部署指南: https://flask.palletsprojects.com/en/latest/deploying/
