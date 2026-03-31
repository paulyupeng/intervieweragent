# 快速配置指南

## 第一步：获取 API 密钥

### 1. Deepgram (语音识别)
1. 访问 https://console.deepgram.com
2. 注册或登录账号
3. 点击 "API Keys"
4. 创建新的 API Key
5. 复制密钥到 `.env` 文件的 `DEEPGRAM_API_KEY`

**新手福利**：注册送 $200 额度

### 2. ElevenLabs (语音合成)
1. 访问 https://elevenlabs.io
2. 注册或登录账号
3. 点击头像 → "Settings"
4. 在 "Profile" 页面找到 API Key
5. 复制密钥到 `.env` 文件的 `ELEVENLABS_API_KEY`

**免费额度**：每月 10,000 字符

### 3. Anthropic (AI 评估)
1. 访问 https://console.anthropic.com
2. 注册或登录账号
3. 创建 API Key
4. 复制密钥到 `.env` 文件的 `ANTHROPIC_API_KEY`

**免费试用**：新账号有免费额度

## 第二步：配置环境变量

1. 复制示例配置：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件：
   ```bash
   # 填入你的 API 密钥
   DEEPGRAM_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

## 第三步：启动服务

### Windows 用户
双击运行 `start.bat`

或者手动执行：
```bash
docker-compose up -d
```

### Mac/Linux 用户
```bash
chmod +x start.sh
./start.sh
```

## 第四步：访问应用

打开浏览器访问：
- **前端**：http://localhost:3000
- **API 文档**：http://localhost:8000/docs

## 第五步：开始面试

1. **添加候选人**：
   - 点击 "Candidates" → "Add Candidate"
   - 填写信息，上传简历（PDF/DOCX）

2. **添加职位描述**：
   - 点击 "Jobs" → "Add Job Description"
   - 粘贴 JD 内容

3. **开始面试**：
   - 点击 "Start Interview"
   - 选择候选人和语言
   - 允许麦克风访问
   - 开始！

## 故障排查

### 容器启动失败
```bash
# 查看日志
docker-compose logs

# 重启服务
docker-compose restart
```

### 数据库连接错误
```bash
# 重置数据库
docker-compose down -v
docker-compose up -d postgres
```

### API 密钥无效
检查 `.env` 文件中的密钥是否正确，没有多余空格

### 麦克风无法使用
- 确保浏览器允许麦克风权限
- 检查系统麦克风设置
- 尝试使用 Chrome 或 Edge 浏览器

## 下一步

- 浏览题库：访问 Admin → Question Banks
- 配置评分权重：访问 Admin → Scoring Configuration
- 查看面试报告：访问 Dashboard → View Results

---

有问题？查看完整文档：README.md
