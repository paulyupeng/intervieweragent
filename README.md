# Interviewer Agent - AI 语音面试系统

一个基于 AI 的互动式在线语音面试系统，可以评估候选人的英文水平、行业理解、专业水平和软技能，并自动记录和打分。

## 功能特性

### 核心功能
- **语音面试**：通过 WebRTC 进行实时语音对话
- **多维度评估**：
  - 英文水平（流利度、词汇、语法、理解力、发音）
  - 行业理解（市场知识、竞争对手认知、法规知识、创新意识）
  - 专业技能（技术能力、问题解决、领域专长、工具熟练度）
  - 软技能（沟通能力、团队合作、领导力、适应性、情商）
- **JD 与简历匹配**：自动解析职位描述和简历，进行匹配度分析
- **题库管理**：支持多语言题库，可自定义问题
- **评分配置**：可定制各维度评分权重
- **面试报告**：自动生成详细的评估报告

### 技术栈
- **前端**：Next.js 14, React, TypeScript, TailwindCSS, LiveKit
- **后端**：FastAPI, Python, asyncpg
- **语音**：Deepgram (STT), ElevenLabs (TTS)
- **LLM**：Anthropic Claude
- **数据库**：PostgreSQL
- **实时通信**：LiveKit (WebRTC)

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：
- `DEEPGRAM_API_KEY` - Deepgram 语音识别
- `ELEVENLABS_API_KEY` - ElevenLabs 语音合成
- `ANTHROPIC_API_KEY` - Anthropic LLM

### 2. 启动服务

```bash
docker-compose up -d
```

服务将在以下地址运行：
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- PostgreSQL：localhost:5432
- LiveKit：ws://localhost:7880

### 3. 访问应用

打开浏览器访问 http://localhost:3000

## 项目结构

```
intervieweragent/
├── backend/
│   ├── app/
│   │   ├── api/              # API 路由
│   │   ├── core/             # 核心配置
│   │   ├── interview/        # 面试引擎
│   │   ├── parser/           # 简历/JD 解析
│   │   ├── services/         # 业务服务
│   │   ├── voice/            # 语音管道
│   │   └── main.py           # FastAPI 入口
│   └── requirements.txt
├── frontend/
│   ├── src/app/              # Next.js 页面
│   └── package.json
├── question_banks/           # 题库 YAML 文件
│   ├── english_proficiency.yaml
│   ├── industry_understanding.yaml
│   ├── professional_skills.yaml
│   └── soft_skills.yaml
├── database/
│   └── init.sql              # 数据库初始化脚本
├── docker-compose.yml
└── .env.example
```

## API 端点

### 面试管理
- `POST /api/interviews/` - 创建面试会话
- `GET /api/interviews/` - 获取面试列表
- `POST /api/interviews/{id}/start` - 开始面试
- `POST /api/interviews/{id}/complete` - 完成面试
- `GET /api/interviews/{id}/evaluation` - 获取评估结果

### 候选人管理
- `POST /api/candidates/` - 创建候选人
- `GET /api/candidates/` - 获取候选人列表
- `POST /api/candidates/{id}/resume` - 上传简历

### 职位描述
- `POST /api/jobs/` - 创建职位描述
- `GET /api/jobs/` - 获取职位列表
- `POST /api/jobs/{id}/parse` - 解析职位要求
- `POST /api/jobs/{id}/match/{candidate_id}` - 匹配候选人与职位

### 题库管理
- `GET /api/questions/banks` - 获取题库列表
- `GET /api/questions/library` - 获取问题库
- `POST /api/questions/` - 添加问题

### 评分系统
- `GET /api/scoring/dimensions` - 获取评分维度
- `POST /api/scoring/scores` - 创建评分
- `GET /api/scoring/configs` - 获取评分配置

## 面试流程

1. **创建/选择候选人**：添加候选人信息并上传简历
2. **选择/创建职位描述**：添加 JD 或直接开始
3. **开始面试**：
   - 系统生成 LiveKit 房间
   - 候选人加入语音通话
   - AI 面试官提问（英文/中文）
4. **自动评估**：
   - 实时转录候选人回答
   - 多维度自动评分
   - LLM 生成综合评估
5. **查看报告**：
   - 总体评分和招聘建议
   - 各维度详细得分
   - 完整面试转录

## 评分系统

### 自动评分指标
- 语速（words per minute）
- 词汇多样性
- 语法错误率
- 填充词计数
- 句子结构复杂度

### LLM 评估
使用 Claude 进行深度评估：
- 回答相关性
- 内容深度
- 例子具体性
- 沟通效果

## 多语言支持

当前支持：
- 英语 (en)
- 中文 (zh)

题库文件命名：
- `english_proficiency.yaml` - 英文题库
- `english_proficiency_zh.yaml` - 中文界面英文回答

## 开发模式

### 单独运行后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 单独运行前端

```bash
cd frontend
npm install
npm run dev
```

## 生产部署

### 环境变量配置

确保在生产环境中设置以下变量：
- `APP_SECRET_KEY` - JWT 签名密钥
- `DATABASE_URL` - 生产数据库连接
- `REDIS_URL` - Redis 连接
- `STORAGE_TYPE=s3` - 使用 S3 存储录音

### Docker 部署

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 获取 API 密钥

### Deepgram
1. 访问 https://console.deepgram.com
2. 注册/登录账号
3. 创建 API Key

### ElevenLabs
1. 访问 https://elevenlabs.io
2. 注册/登录账号
3. 在 Settings 获取 API Key

### Anthropic
1. 访问 https://console.anthropic.com
2. 注册/登录账号
3. 创建 API Key

## 常见问题

### Q: 面试录音保存在哪里？
A: 默认保存在 `backend/recordings/` 目录，可配置 S3 存储。

### Q: 如何自定义题库？
A: 编辑 `question_banks/` 目录下的 YAML 文件，或通过 Admin 界面管理。

### Q: 评分权重如何调整？
A: 在 Admin > Scoring Configuration 页面调整各维度权重。

### Q: 支持电话面试吗？
A: 当前版本仅支持 WebRTC 网页面试，电话集成（Twilio）在开发中。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**Version**: 1.0.0
**Author**: Interviewer Agent Team
**Date**: 2026-03-31
