# 📤 项目导出 - 快速指南

## 当前项目位置
`C:\Users\pauly\intervieweragent`

---

## 方法 1：ZIP 打包（最简单）

### Windows 一键打包

双击运行：
```
export.bat
```

或在项目目录打开命令行执行：
```powershell
powershell -Command "Compress-Archive -Path 'backend','frontend','question_banks','database','.env.example','docker-compose.yml','README.md','QUICKSTART.md','.gitignore' -DestinationPath 'exports\interviewer-agent-export.zip' -Force"
```

生成的文件：`exports\interviewer-agent-export.zip`

---

## 方法 2：Git（适合持续开发）

### 初始化仓库
```bash
cd C:\Users\pauly\intervieweragent
git init
git add -A
git commit -m "Initial commit"
```

### 推送到远程（可选）
```bash
# GitHub
git remote add origin https://github.com/你的用户名/intervieweragent.git
git push -u origin main

# Gitee（国内）
git remote add origin https://gitee.com/你的用户名/intervieweragent.git
git push -u origin main
```

### 在新电脑克隆
```bash
git clone https://github.com/你的用户名/intervieweragent.git
cd intervieweragent
cp .env.example .env
# 编辑 .env 填入 API 密钥
docker-compose up -d
```

---

## 方法 3：直接复制整个文件夹

直接用文件管理器复制整个 `intervieweragent` 文件夹到：
- USB 闪存盘
- 网络共享文件夹
- 云同步文件夹（OneDrive/Google Drive）

---

## ⚠️ 重要：API 密钥处理

### 选项 A：复制现有 .env 文件
```bash
# 在原电脑
copy C:\Users\pauly\intervieweragent\.env D:\U 盘\

# 在新电脑
copy D:\U 盘\.env C:\新路径\intervieweragent\
```

### 选项 B：在新电脑重新配置
```bash
cp .env.example .env
# 用文本编辑器打开 .env 填入 API 密钥
```

---

## 在新电脑启动

### 前提条件
确保新电脑已安装：
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 启动命令
```bash
# Windows - 双击
start.bat

# 或命令行
cd intervieweragent
docker-compose up -d
```

### 验证
- 前端：http://localhost:3000
- API: http://localhost:8000
- API 文档：http://localhost:8000/docs

---

## 文件清单

### 必须复制的核心文件
| 文件/目录 | 大小约 | 说明 |
|----------|-------|------|
| `backend/` | 50KB | 后端代码 |
| `frontend/` | 100KB | 前端代码 |
| `question_banks/` | 30KB | 题库 |
| `database/init.sql` | 10KB | 数据库结构 |
| `docker-compose.yml` | 2KB | 服务编排 |
| `.env` | 1KB | **你的 API 密钥** |

### 不需要复制（可重新生成）
- `node_modules/` - 运行 `npm install` 自动生成
- `__pycache__/` - Python 缓存
- `.next/` - Next.js 构建输出

---

## 传输方式对比

| 方式 | 速度 | 便利性 | 适用场景 |
|------|-----|--------|---------|
| USB 闪存盘 | ⭐⭐⭐ | ⭐⭐⭐ | 无网络环境 |
| 微信/QQ | ⭐⭐ | ⭐⭐⭐ | 小文件快速传输 |
| 云存储 | ⭐⭐ | ⭐⭐ | 跨设备同步 |
| Git | ⭐ | ⭐⭐⭐ | 持续开发协作 |
| 局域网共享 | ⭐⭐⭐ | ⭐⭐ | 同网络多设备 |

---

## 常见问题

**Q: 新电脑 Docker 启动失败？**
- 确保 Docker Desktop 已安装并运行
- Windows 需要启用 WSL2

**Q: 端口被占用？**
- 编辑 `docker-compose.yml` 修改端口映射
- 或关闭占用 3000/8000/5432 端口的程序

**Q: 没有 API 密钥能用吗？**
- 基础功能可以用（面试、录音）
- 但 LLM 评估和部分高级功能需要密钥

---

**需要帮助？** 查看完整文档：`MIGRATION_GUIDE.md`
