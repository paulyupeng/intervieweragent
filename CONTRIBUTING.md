# 贡献指南

感谢你为 Interviewer Agent 项目做出贡献！

本指南旨在帮助你更好地参与项目开发。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [代码风格](#代码风格)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [问题报告](#问题报告)
- [功能建议](#功能建议)

---

## 行为准则

请遵循以下原则：

- **尊重他人**：无论技术水平、背景如何，都要以礼相待
- **建设性讨论**：专注于问题和解决方案，而非人身攻击
- **开放包容**：欢迎各种形式的贡献，包括代码、文档、测试、翻译等

---

## 如何贡献

### 1. Fork 仓库

访问 https://github.com/paulyupeng/intervieweragent 并 Fork

### 2. 克隆到本地

```bash
git clone https://github.com/你的用户名/intervieweragent.git
cd intervieweragent
```

### 3. 创建分支

```bash
# 功能分支
git checkout -b feature/your-feature-name

# 或修复分支
git checkout -b fix/your-bug-fix
```

### 4. 进行更改

编写代码、文档或测试。

### 5. 提交更改

```bash
git add .
git commit -m "feat: 添加你的功能"
```

### 6. 推送到远程

```bash
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

在 GitHub 上：
1. 访问你的 Fork 仓库
2. 点击 "Pull requests" → "New pull request"
3. 填写描述，提交

---

## 开发环境设置

### 前置要求

- Python 3.11+
- Node.js 20+
- Docker Desktop

### 后端设置

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
# 编辑 .env 填入 API 密钥
uvicorn app.main:app --reload
```

### 前端设置

```bash
cd frontend
npm install
npm run dev
```

### 数据库设置

```bash
# 使用 Docker 启动数据库
docker-compose up -d postgres

# 或本地安装 PostgreSQL
psql -U postgres -c "CREATE DATABASE interviewer;"
```

---

## 代码风格

### Python

- 遵循 [PEP 8](https://pep8.org/)
- 使用类型注解
- 使用 `black` 格式化

```bash
# 安装工具
pip install black flake8 mypy

# 格式化
black backend/app/

# 检查
flake8 backend/app/ --max-line-length=120
```

### TypeScript

- 使用 ESLint + Prettier
- 严格类型检查

```bash
cd frontend
npm run lint
npm run format
```

### 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具/配置

**示例：**
```
feat(interview): 添加追问功能

- 实现基于关键词的追问触发
- 添加追问配置界面

Closes #123
```

---

## Pull Request 流程

### PR 标题规范

```
feat: 添加新功能
fix: 修复某某问题
docs: 更新文档
```

### PR 描述模板

```markdown
## 描述
简要描述此 PR 的目的

## 相关 Issue
Closes #123

## 更改内容
- [ ] 添加了某某功能
- [ ] 修复了某某问题
- [ ] 更新了文档

## 测试
描述如何测试这些更改

## 截图（如适用）
[截图或录屏]
```

### 审核流程

1. **CI 检查**：确保所有 CI 检查通过
2. **代码审查**：至少 1 名维护者审核
3. **测试**：在本地测试功能
4. **合并**：审核通过后合并

---

## 问题报告

### 提交 Issue 前

- 搜索现有 Issue，避免重复
- 确认问题在最新版本中存在
- 收集错误信息和复现步骤

### Issue 模板

```markdown
### 问题描述
简要描述遇到的问题

### 复现步骤
1. 启动服务
2. 点击某某按钮
3. 输入某某内容
4. 出现错误

### 期望行为
应该发生什么

### 实际行为
实际发生了什么

### 环境信息
- OS: Windows 11
- Python: 3.11
- Node.js: 20
- Docker: 最新版

### 日志/截图
[粘贴日志或截图]
```

---

## 功能建议

### 提交建议前

- 搜索现有 Issue，确认未被提出
- 思考功能的目的和价值

### 建议模板

```markdown
### 功能描述
简要描述建议的功能

### 目的
为什么需要这个功能？解决什么问题？

### 实现建议
如何实现？（可选）

### 替代方案
有没有其他解决方案？（可选）

### 额外信息
任何相关截图、设计稿等
```

---

## 文档贡献

文档与代码同样重要！欢迎贡献：

- 修复拼写错误
- 补充说明
- 翻译文档
- 添加示例

---

## 测试贡献

- 编写单元测试
- 编写集成测试
- 手动测试新功能
- 报告 Bug

---

## 问答

**Q: 我的 PR 多久会被审核？**
A: 通常 1-3 个工作日，请耐心等待

**Q: 如何与 maintainer 沟通？**
A: 在 Issue 或 PR 中留言，或发送邮件至 Paul.yupeng@gmail.com

**Q: 我可以添加新功能吗？**
A: 可以！请先开 Issue 讨论，确认方向后再开发

---

## 致谢

感谢所有贡献者！

<a href="https://github.com/paulyupeng/intervieweragent/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=paulyupeng/intervieweragent" />
</a>

---

[返回顶部](#贡献指南)
