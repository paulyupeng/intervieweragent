# GitHub 配置指南

## 前提条件

需要安装 **GitHub CLI** (`gh`) 工具。

### 安装 GitHub CLI

**Windows:**
```powershell
# 使用 winget
winget install GitHub.cli

# 或下载 installer
# https://github.com/cli/cli/releases/latest
```

**Mac:**
```bash
brew install gh
```

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

---

## 一键配置 GitHub（推荐）

### Windows 用户
双击运行：
```
setup-github.bat
```

### Mac/Linux 用户
```bash
chmod +x setup-github.sh
./setup-github.sh
```

脚本会自动：
1. 检查是否安装 `gh` 工具
2. 引导 GitHub 登录认证
3. 创建新仓库
4. 推送代码到 GitHub

---

## 手动配置步骤

如果不想用脚本，可以手动执行：

### 1. 登录 GitHub

```bash
gh auth login
```

按提示操作：
- 选择 "GitHub.com"
- 选择 "HTTPS"
- 选择 "Login with a web browser"
- 复制代码并在浏览器打开 github.com 进行授权

### 2. 创建仓库

```bash
# 创建公开仓库
gh repo create intervieweragent --public --source=. --remote=origin --push

# 或创建私有仓库
gh repo create intervieweragent --private --source=. --remote=origin --push
```

### 3. 验证

```bash
# 查看远程仓库
git remote -v

# 应该看到：
# origin  https://github.com/你的用户名/intervieweragent.git (fetch)
# origin  https://github.com/你的用户名/intervieweragent.git (push)
```

---

## 后续常用命令

### 推送更改
```bash
git add .
git commit -m "feat: 添加新功能"
git push
```

### 拉取更新
```bash
git pull
```

### 查看状态
```bash
git status
git log --oneline
```

### 创建分支
```bash
# 创建并切换分支
git checkout -b feature/new-feature

# 推送分支到远程
git push -u origin feature/new-feature
```

### 创建 Pull Request
```bash
gh pr create --title "添加新功能" --body "描述你的更改"
```

---

## 在 GitHub 上管理项目

### 1. 访问你的仓库

打开浏览器访问：
```
https://github.com/你的用户名/intervieweragent
```

### 2. 添加仓库信息

在 GitHub 仓库页面：
- 点击 "About" 区域右侧的⚙️图标
- 添加描述：`AI-powered voice interview system for candidate assessment`
- 添加网站链接（如果有）
- 添加 Topics：`ai`, `interview`, `voice`, `fastapi`, `nextjs`, `webrtc`, `candidate-assessment`

### 3. 添加 README 徽章

在 README.md 顶部添加：

```markdown
![GitHub stars](https://img.shields.io/github/stars/你的用户名/intervieweragent?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/你的用户名/intervieweragent?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/你的用户名/intervieweragent?style=for-the-badge)
```

### 4. 启用 GitHub Actions（可选）

在仓库 Settings → Actions 中启用 CI/CD。

---

## 从任何地方克隆项目

配置完成后，你可以在任何电脑上克隆项目：

```bash
git clone https://github.com/你的用户名/intervieweragent.git
cd intervieweragent
cp .env.example .env
# 编辑 .env 填入 API 密钥
docker-compose up -d
```

---

## 邀请协作者

### 添加协作者
1. 访问仓库 Settings
2. 点击 "Collaborators"
3. 点击 "Add people"
4. 输入对方的 GitHub 用户名或邮箱

### 协作者克隆
```bash
# 协作者可以克隆并贡献
git clone https://github.com/你的用户名/intervieweragent.git
```

---

## 从其他分支恢复 .env 文件

`.env` 文件（包含 API 密钥）已在 `.gitignore` 中，不会被提交。

在新电脑或新分支使用时：
```bash
cp .env.example .env
# 手动编辑 .env 填入你的 API 密钥
```

---

## 故障排查

### Q: `gh` 命令找不到
A: 确保已安装 GitHub CLI 并添加到 PATH

### Q: 认证失败
A: 尝试 `gh auth logout` 然后重新 `gh auth login`

### Q: 仓库已存在
A: 使用不同的仓库名，或连接现有仓库：
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### Q: 推送失败
A: 检查认证状态：`gh auth status`

---

## 下一步

1. ✅ 运行 `setup-github.bat` 或 `setup-github.sh`
2. ✅ 访问 GitHub 查看你的仓库
3. ✅ 添加仓库描述和 Topics
4. ✅ 分享给协作者或公开给社区

有问题？查看官方文档：https://cli.github.com/manual/
