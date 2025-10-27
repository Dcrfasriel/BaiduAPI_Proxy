#!/bin/bash

# 百度搜索转接服务部署脚本

echo "======================================"
echo "开始部署百度搜索转接服务"
echo "======================================"

# 1. 初始化Git仓库（如果还没有）
if [ ! -d .git ]; then
    echo "初始化Git仓库..."
    git init
    git add .
    git commit -m "Initial commit: 百度搜索转接服务"
else
    echo "Git仓库已存在，跳过初始化"
fi

# 2. 提示用户创建GitHub仓库
echo ""
echo "请按照以下步骤操作："
echo "1. 访问 https://github.com/new 创建新仓库"
echo "2. 仓库名称建议: baidu-search-proxy"
echo "3. 不要初始化README, .gitignore或license"
echo "4. 创建完成后，复制仓库URL"
echo ""
read -p "请输入GitHub仓库URL (例如: https://github.com/username/repo.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "错误: 未输入仓库URL"
    exit 1
fi

# 3. 添加远程仓库
echo "添加远程仓库..."
git remote add origin $REPO_URL 2>/dev/null || git remote set-url origin $REPO_URL

# 4. 推送到GitHub
echo "推送代码到GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "======================================"
echo "代码已推送到GitHub！"
echo "======================================"
echo ""
echo "接下来选择部署平台："
echo ""
echo "方式1 - Render.com (推荐):"
echo "  1. 访问 https://render.com"
echo "  2. 注册并登录"
echo "  3. 点击 'New' -> 'Web Service'"
echo "  4. 连接GitHub并选择刚才的仓库"
echo "  5. 配置："
echo "     - Build Command: pip install -r requirements.txt"
echo "     - Start Command: python search_proxy.py"
echo "  6. 点击 'Create Web Service'"
echo ""
echo "方式2 - Railway.app:"
echo "  1. 访问 https://railway.app"
echo "  2. 使用GitHub登录"
echo "  3. 点击 'New Project' -> 'Deploy from GitHub repo'"
echo "  4. 选择刚才的仓库"
echo "  5. Railway会自动检测并部署"
echo ""
echo "部署完成后，您将获得一个公网URL！"
echo "======================================"
