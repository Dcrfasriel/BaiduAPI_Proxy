# 百度搜索转接服务部署脚本 (PowerShell)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "开始部署百度搜索转接服务" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查Git是否安装
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装Git，请先安装Git" -ForegroundColor Red
    Write-Host "下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# 2. 初始化Git仓库（如果还没有）
if (!(Test-Path .git)) {
    Write-Host "初始化Git仓库..." -ForegroundColor Green
    git init
    git add .
    git commit -m "Initial commit: 百度搜索转接服务"
} else {
    Write-Host "Git仓库已存在，跳过初始化" -ForegroundColor Yellow
}

# 3. 提示用户创建GitHub仓库
Write-Host ""
Write-Host "请按照以下步骤操作：" -ForegroundColor Yellow
Write-Host "1. 访问 https://github.com/new 创建新仓库" -ForegroundColor White
Write-Host "2. 仓库名称建议: baidu-search-proxy" -ForegroundColor White
Write-Host "3. 不要初始化README, .gitignore或license" -ForegroundColor White
Write-Host "4. 创建完成后，复制仓库URL" -ForegroundColor White
Write-Host ""

$repoUrl = Read-Host "请输入GitHub仓库URL (例如: https://github.com/username/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "错误: 未输入仓库URL" -ForegroundColor Red
    exit 1
}

# 4. 添加远程仓库
Write-Host "添加远程仓库..." -ForegroundColor Green
try {
    git remote add origin $repoUrl 2>$null
} catch {
    git remote set-url origin $repoUrl
}

# 5. 推送到GitHub
Write-Host "推送代码到GitHub..." -ForegroundColor Green
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "代码已推送到GitHub！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 6. 显示部署选项
Write-Host "接下来选择部署平台：" -ForegroundColor Yellow
Write-Host ""
Write-Host "方式1 - Render.com (推荐):" -ForegroundColor Cyan
Write-Host "  1. 访问 https://render.com" -ForegroundColor White
Write-Host "  2. 注册并登录" -ForegroundColor White
Write-Host "  3. 点击 'New' -> 'Web Service'" -ForegroundColor White
Write-Host "  4. 连接GitHub并选择刚才的仓库" -ForegroundColor White
Write-Host "  5. 配置：" -ForegroundColor White
Write-Host "     - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "     - Start Command: python search_proxy.py" -ForegroundColor Gray
Write-Host "  6. 点击 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "方式2 - Railway.app:" -ForegroundColor Cyan
Write-Host "  1. 访问 https://railway.app" -ForegroundColor White
Write-Host "  2. 使用GitHub登录" -ForegroundColor White
Write-Host "  3. 点击 'New Project' -> 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "  4. 选择刚才的仓库" -ForegroundColor White
Write-Host "  5. Railway会自动检测并部署" -ForegroundColor White
Write-Host ""
Write-Host "方式3 - Vercel (需要配置serverless):" -ForegroundColor Cyan
Write-Host "  1. 访问 https://vercel.com" -ForegroundColor White
Write-Host "  2. 使用GitHub登录" -ForegroundColor White
Write-Host "  3. Import项目" -ForegroundColor White
Write-Host "  4. 选择刚才的仓库并部署" -ForegroundColor White
Write-Host ""
Write-Host "部署完成后，您将获得一个公网URL！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$openBrowser = Read-Host "是否打开Render.com进行部署？(Y/N)"
if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
    Start-Process "https://render.com"
}
