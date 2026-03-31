# 迁移指南 - 如何将项目导出到另一台电脑

## 方法 1：ZIP/TAR 打包（推荐用于离线传输）

### 在当前电脑导出

**Windows 用户：**
```bash
# 双击运行
export.bat
```
或手动执行：
```bash
powershell -Command "Compress-Archive -Path '.\backend', '.\frontend', '.\question_banks', '.\database', '.env.example', 'docker-compose.yml', 'README.md', 'QUICKSTART.md', '.gitignore' -DestinationPath '.\exports\interviewer-agent-export.zip' -Force"
```

**Linux/Mac 用户：**
```bash
chmod +x export.sh
./export.sh
```

生成的文件：
- Windows: `exports/interviewer-agent-export.zip`
- Linux/Mac: `exports/interviewer-agent-export.tar.gz`

### 传输文件

使用以下任一方式传输到目标电脑：
- USB 闪存盘
- 局域网共享
- 云存储（Google Drive、OneDrive 等）
- 微信/QQ 文件传输

### 在目标电脑导入

1. **解压文件**到新目录

2. **复制你的 API 密钥配置**（二选一）：
   ```bash
   # 方式 A：从原电脑复制整个.env 文件
   cp /原电脑路径/.env .

   # 方式 B：在新电脑创建.env 文件
   cp .env.example .env
   # 然后编辑 .env 填入你的 API 密钥
   ```

3. **安装 Docker Desktop**（如果目标电脑没有）：
   - Windows: https://docker.com/products/docker-desktop
   - Mac: 同上
   - Linux: `apt-get install docker.io docker-compose`

4. **启动服务**：
   ```bash
   # Windows
   start.bat

   # Linux/Mac
   ./start.sh

   # 或手动启动
   docker-compose up -d
   ```

5. **访问应用**：http://localhost:3000

---

## 方法 2：Git 版本控制（推荐用于持续开发）

### 在当前电脑初始化 Git

```bash
cd intervieweragent

# 初始化仓库
git init

# 添加所有文件
git add -A

# 创建提交
git commit -m "Initial commit - Interviewer Agent v1.0"
```

### 推送到远程仓库

**选项 A：GitHub**
```bash
# 创建新仓库后执行
git remote add origin https://github.com/你的用户名/intervieweragent.git
git branch -M main
git push -u origin main
```

**选项 B：Gitee（国内更快）**
```bash
git remote add origin https://gitee.com/你的用户名/intervieweragent.git
git push -u origin main
```

**选项 C：本地 Git 服务器**
```bash
git clone --bare /path/to/repo.git /shared/folder/intervieweragent.git
```

### 在目标电脑克隆

```bash
# 从 GitHub
git clone https://github.com/你的用户名/intervieweragent.git

# 从 Gitee
git clone https://gitee.com/你的用户名/intervieweragent.git

# 进入目录
cd intervieweragent

# 配置环境
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 启动
docker-compose up -d
```

---

## 方法 3：Docker 镜像（最完整的环境迁移）

### 在当前电脑创建镜像

```bash
# 构建后端镜像
docker build -t interviewer-agent-backend ./backend

# 构建前端镜像
docker build -t interviewer-agent-frontend ./frontend

# 保存镜像到文件
docker save interviewer-agent-backend -o backend-image.tar
docker save interviewer-agent-frontend -o frontend-image.tar
```

### 传输镜像

```bash
# 压缩镜像
tar -czvf interviewer-images.tar.gz backend-image.tar frontend-image.tar

# 传输到目标电脑（scp、rsync、USB 等）
```

### 在目标电脑加载

```bash
# 解压并加载镜像
tar -xzf interviewer-images.tar.gz
docker load -i backend-image.tar
docker load -i frontend-image.tar

# 启动服务
docker-compose up -d
```

---

## 方法 4：使用项目同步脚本

创建一个同步脚本 `sync.sh`：

```bash
#!/bin/bash
# 同步到目标电脑（通过局域网）

TARGET_HOST="192.168.1.100"  # 目标电脑 IP
TARGET_PATH="/home/user/intervieweragent"

rsync -avz --exclude='.claude' --exclude='node_modules' \
    --exclude='__pycache__' --exclude='.next' \
    ./ ${TARGET_HOST}:${TARGET_PATH}/

echo "Sync complete!"
```

---

## 重要提醒

### 必须迁移的文件

| 文件/目录 | 重要性 | 说明 |
|----------|--------|------|
| `backend/` | ⭐⭐⭐ | 后端核心代码 |
| `frontend/` | ⭐⭐⭐ | 前端核心代码 |
| `question_banks/` | ⭐⭐⭐ | 题库配置 |
| `database/` | ⭐⭐⭐ | 数据库结构 |
| `docker-compose.yml` | ⭐⭐⭐ | 服务编排 |
| `.env` | ⭐⭐⭐ | **包含 API 密钥** |
| `README.md` | ⭐⭐ | 文档 |

### 不需要迁移的文件

- `node_modules/` - 可在目标电脑 `npm install` 重新安装
- `__pycache__/` - Python 缓存
- `.next/` - Next.js 构建产物
- `.claude/` - 本地 Claude 配置
- `recordings/` - 面试录音（可选）
- `*.db`, `*.sqlite` - 本地数据库（可选）

---

## 在目标电脑验证

```bash
# 检查所有服务是否运行
docker-compose ps

# 应该看到：
# NAME                    STATUS
# interview-backend       Up
# interview-frontend      Up
# interview-postgres      Up
# interview-redis         Up
# interview-livekit       Up

# 测试后端
curl http://localhost:8000/health

# 测试前端
# 浏览器打开 http://localhost:3000
```

---

## 常见问题

### Q: 目标电脑 Docker 启动失败？
A: 确保 Docker Desktop 已正确安装并运行。Windows 用户需要启用 WSL2。

### Q: 端口冲突？
A: 如果 3000/8000/5432 端口被占用，编辑 `docker-compose.yml` 修改端口映射。

### Q: API 密钥无效？
A: 确保 `.env` 文件中的 API 密钥正确，没有多余空格。

### Q: 数据库为空？
A: 首次启动会自动初始化数据库。如需重置：`docker-compose down -v && docker-compose up -d`

---

## 推荐方案

| 场景 | 推荐方法 |
|------|---------|
| 一次性迁移 | 方法 1：ZIP 打包 |
| 持续协作开发 | 方法 2：Git 版本控制 |
| 环境完全一致 | 方法 3：Docker 镜像 |
| 频繁同步 | 方法 4：Rsync 脚本 |
