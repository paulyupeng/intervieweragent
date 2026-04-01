# Interviewer Agent - AI 语音面试系统

[![GitHub stars](https://img.shields.io/github/stars/paulyupeng/intervieweragent?style=for-the-badge&logo=github)](https://github.com/paulyupeng/intervieweragent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/paulyupeng/intervieweragent?style=for-the-badge&logo=github)](https://github.com/paulyupeng/intervieweragent/network)
[![GitHub license](https://img.shields.io/github/license/paulyupeng/intervieweragent?style=for-the-badge)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/paulyupeng/intervieweragent?style=for-the-badge&logo=github)](https://github.com/paulyupeng/intervieweragent/issues)

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-✅-blue?style=for-the-badge&logo=docker)](https://www.docker.com/)

> 🎙️ 一个基于 AI 的互动式在线语音面试系统，自动评估候选人的英文水平、行业理解、专业技能和软技能

---

## 📋 目录

- [功能特性](#-功能特性)
- [技术架构](#-技术架构)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [API 文档](#-api-文档)
- [面试流程](#-面试流程)
- [评分系统](#-评分系统)
- [多语言支持](#-多语言支持)
- [开发指南](#-开发指南)
- [部署指南](#-部署指南)
- [常见问题](#-常见问题)
- [路线图](#-路线图)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 核心功能

| 功能 | 描述 |
|------|------|
| 🎤 **语音面试** | 通过 WebRTC 进行实时语音对话，低延迟、高质量 |
| 📊 **多维度评估** | 英文水平、行业理解、专业技能、软技能四大维度 |
| 📄 **JD-简历匹配** | 自动解析职位描述和简历，智能匹配度分析 |
| 📝 **题库管理** | 55+ 道精选题目，支持多语言、自定义 |
| ⚖️ **评分配置** | 可定制各维度评分权重，灵活适配不同岗位 |
| 📈 **面试报告** | 自动生成详细评估报告，支持导出 |

### 评估维度详解

#### 1. English Proficiency (英文水平)
- **Fluency** - 流利度：语速、停顿、连贯性
- **Vocabulary** - 词汇：多样性、准确性、专业性
- **Grammar** - 语法：句式结构、时态、语态
- **Comprehension** - 理解力：问题理解、回答相关性
- **Pronunciation** - 发音：清晰度、可懂度

#### 2. Industry Understanding (行业理解)
- **Market Knowledge** - 市场认知：行业趋势、市场规模
- **Competitor Awareness** - 竞争格局：主要玩家、差异化
- **Regulatory Knowledge** - 法规意识：合规要求、政策环境
- **Innovation Awareness** - 创新意识：新技术、新趋势

#### 3. Professional Skills (专业技能)
- **Technical Competency** - 技术能力：专业知识、硬技能
- **Problem Solving** - 问题解决：分析能力、解决方案
- **Domain Expertise** - 领域专长：深度、广度
- **Tool Proficiency** - 工具熟练度：框架、平台、工具链

#### 4. Soft Skills (软技能)
- **Communication** - 沟通能力：表达清晰、逻辑性强
- **Teamwork** - 团队合作：协作精神、冲突处理
- **Leadership** - 领导力：影响力、决策能力
- **Adaptability** - 适应性：变化应对、学习敏捷
- **Emotional Intelligence** - 情商：自我认知、同理心

---

## 🏗️ 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Interviewer Agent                       │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Next.js 14 + React + TypeScript)                     │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │   Interview Room    │  │    Admin Dashboard  │              │
│  │   (WebRTC + LiveKit)│  │    (Charts + Reports)│             │
│  └─────────────────────┘  └─────────────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  Backend (FastAPI + Python 3.11)                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Interview API  │  │   Scoring API   │  │   Question API  │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │  Interview Engine │  │  Voice Pipeline │  │   JD Parser   │ │
│  │  (State Machine) │  │  (STT + TTS)    │  │  (PDF/DOCX)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  External Services                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Deepgram    │  │  ElevenLabs  │  │   Anthropic  │         │
│  │  (Speech→Text)│  │  (Text→Speech)│  │   (Claude)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐                           │
│  │  LiveKit     │  │  PostgreSQL  │                           │
│  │  (WebRTC)    │  │  (Data Store)│                           │
│  └──────────────┘  └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **前端** | Next.js, React, TypeScript | 14.x |
| **样式** | TailwindCSS | 3.x |
| **实时通信** | LiveKit, WebRTC | 2.x |
| **后端** | FastAPI, Python | 0.109+, 3.11+ |
| **数据库** | PostgreSQL, asyncpg | 15+, 0.29+ |
| **缓存** | Redis | 7.x |
| **语音识别** | Deepgram | Nova-2 |
| **语音合成** | ElevenLabs | v1 |
| **LLM** | Anthropic Claude | Sonnet 4 |
| **部署** | Docker, Docker Compose | Latest |

---

## 🚀 快速开始

### 前置要求

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (最新版)
- Git (可选，用于版本控制)

### 1. 克隆项目

```bash
git clone https://github.com/paulyupeng/intervieweragent.git
cd intervieweragent
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入 API 密钥：

```bash
# API Keys
DEEPGRAM_API_KEY=your_deepgram_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

> 💡 **获取 API 密钥**：详见 [API 密钥获取指南](#-获取-api-密钥)

### 3. 启动服务

**Windows 用户：**
```bash
start.bat
```

**Mac/Linux 用户：**
```bash
chmod +x start.sh
./start.sh
```

或手动启动：
```bash
docker-compose up -d
```

### 4. 访问应用

| 服务 | URL |
|------|-----|
| 🌐 前端 | http://localhost:3000 |
| 📡 API 文档 | http://localhost:8000/docs |
| 🗄️ PostgreSQL | localhost:5432 |
| 🔴 Redis | localhost:6379 |
| 📡 LiveKit | ws://localhost:7880 |

---

## 📁 项目结构

```
intervieweragent/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # REST API 路由
│   │   │   ├── auth.py        # 认证接口
│   │   │   ├── candidates.py  # 候选人管理
│   │   │   ├── interviews.py  # 面试管理
│   │   │   ├── job_descriptions.py  # JD 管理
│   │   │   ├── questions.py   # 题库管理
│   │   │   └── scoring.py     # 评分管理
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 应用配置
│   │   │   └── database.py    # 数据库连接
│   │   ├── interview/         # 面试引擎
│   │   │   ├── engine.py      # 面试流程编排
│   │   │   └── scoring.py     # 评分服务
│   │   ├── parser/            # 解析器
│   │   │   └── resume_parser.py  # 简历/JD 解析
│   │   ├── services/          # 业务服务
│   │   │   └── interview_service.py
│   │   ├── voice/             # 语音处理
│   │   │   └── pipeline.py    # STT/TTS 管道
│   │   ├── main.py            # FastAPI 入口
│   │   └── schemas.py         # Pydantic 模型
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile
│
├── frontend/                   # Next.js 前端
│   ├── src/app/
│   │   ├── admin/page.tsx     # 管理后台
│   │   ├── candidates/page.tsx # 候选人管理
│   │   ├── dashboard/page.tsx  # 仪表板
│   │   ├── interview/
│   │   │   ├── results/page.tsx  # 面试结果
│   │   │   ├── room/page.tsx     # 面试房间
│   │   │   └── start/page.tsx    # 开始面试
│   │   ├── jobs/page.tsx      # 职位描述管理
│   │   ├── settings/page.tsx  # 设置
│   │   ├── layout.tsx         # 根布局
│   │   └── page.tsx           # 首页
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── question_banks/            # 题库
│   ├── english_proficiency.yaml
│   ├── english_proficiency_zh.yaml
│   ├── industry_understanding.yaml
│   ├── professional_skills.yaml
│   └── soft_skills.yaml
│
├── database/
│   └── init.sql               # 数据库初始化脚本
│
├── docker-compose.yml         # Docker 编排
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略文件
├── LICENSE                   # MIT 许可证
├── README.md                 # 本文件
├── QUICKSTART.md             # 快速配置指南
├── MIGRATION_GUIDE.md        # 迁移指南
└── PROJECT_SUMMARY.md        # 项目总结
```

---

## 📡 API 文档

启动项目后访问 http://localhost:8000/docs 查看完整的 Swagger 文档。

### 主要 API 端点

#### 面试管理 (Interviews)

```bash
# 创建面试会话
POST /api/interviews/
{
  "candidate_id": "uuid",
  "job_description_id": "uuid",
  "language": "en"
}

# 获取面试列表
GET /api/interviews/?status=completed&limit=50

# 开始面试（获取 LiveKit token）
POST /api/interviews/{session_id}/start

# 完成面试
POST /api/interviews/{session_id}/complete

# 获取评估报告
GET /api/interviews/{session_id}/evaluation
```

#### 候选人管理 (Candidates)

```bash
# 创建候选人（支持简历上传）
POST /api/candidates/
Content-Type: multipart/form-data
- name: "John Doe"
- email: "john@example.com"
- resume: (file)

# 获取候选人列表
GET /api/candidates/

# 获取候选人详情
GET /api/candidates/{candidate_id}
```

#### 职位描述 (Job Descriptions)

```bash
# 创建职位描述
POST /api/jobs/
- title: "Senior Software Engineer"
- company: "Tech Corp"
- jd_text: "..."

# 解析 JD（提取结构化要求）
POST /api/jobs/{jd_id}/parse

# 匹配候选人与 JD
POST /api/jobs/{jd_id}/match/{candidate_id}
```

#### 题库管理 (Questions)

```bash
# 获取题库列表
GET /api/questions/banks?category=english_proficiency&language=en

# 获取题库详情（含题目）
GET /api/questions/banks/{bank_id}

# 获取题目库（从 YAML 文件加载）
GET /api/questions/library?language=en
```

#### 评分系统 (Scoring)

```bash
# 获取评分维度
GET /api/scoring/dimensions?category=english_proficiency

# 创建/更新评分
POST /api/scoring/scores
{
  "interview_session_id": "uuid",
  "dimension_id": "uuid",
  "score": 8.5,
  "max_score": 10.0
}

# 获取评分配置
GET /api/scoring/configs
```

---

## 🎬 面试流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      Interview Workflow                         │
│                                                                 │
│  1. Create Candidate    2. Select/Upload JD   3. Start Interview│
│         ↓                     ↓                      ↓          │
│  ┌──────────┐          ┌──────────┐         ┌──────────┐       │
│  │ Candidate│          │   Job    │         │ LiveKit  │       │
│  │  Profile │          │Description│         │  Room    │       │
│  └──────────┘          └──────────┘         └──────────┘       │
│                                                ↓                │
│  6. View Report ←── 5. Generate Evaluation ← 4. Q&A Session    │
│         ↓                    ↓                      ↓          │
│  ┌──────────┐          ┌──────────┐         ┌──────────┐       │
│  │Dashboard │          │   LLM    │         │   AI     │       │
│  │  & Export│          │ Scoring  │         │Interviewer│      │
│  └──────────┘          └──────────┘         └──────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 详细步骤

| 步骤 | 操作 | 输出 |
|------|------|------|
| 1 | 创建/选择候选人 | 候选人档案 |
| 2 | 上传/选择 JD（可选） | 职位需求分析 |
| 3 | 开始面试 | LiveKit 房间 Token |
| 4 | AI 提问 → 候选人回答 | 录音 + 转录文本 |
| 5 | 自动评分 + LLM 评估 | 多维度分数 + 建议 |
| 6 | 查看报告 | 可导出的评估报告 |

---

## ⚖️ 评分系统

### 自动评分指标（40%）

| 指标 | 计算方法 | 权重 |
|------|----------|------|
| 语速 | Words Per Minute (目标：120-150) | 10% |
| 词汇多样性 | Unique Word Ratio | 10% |
| 语法错误率 | 错误数 / 总词数 | 10% |
| 填充词计数 | um, uh, like 出现次数 | 5% |
| 句子复杂度 | 平均句长 + 从句数量 | 5% |

### LLM 评估（60%）

使用 Anthropic Claude 进行深度评估：

```python
# 评估 prompt 示例
prompt = f"""
Evaluate the interview response on these dimensions:

Question: {question_text}
Candidate Response: {transcript}

Rate each dimension (0-10 scale):
- Fluency: Speech flow, hesitation, pace
- Vocabulary: Range and precision
- Grammar: Sentence structure accuracy
- Comprehension: Understanding and relevance
- Content Quality: Depth, examples, specificity
"""
```

### 评分输出示例

```json
{
  "overall_score": 78.5,
  "hiring_recommendation": "PROCEED",
  "dimension_scores": {
    "english_proficiency": {
      "score": 82.0,
      "max_score": 100.0,
      "breakdown": {
        "fluency": 85,
        "vocabulary": 80,
        "grammar": 78,
        "comprehension": 85,
        "pronunciation": 80
      }
    },
    "industry_understanding": { "score": 75.0, ... },
    "professional_skills": { "score": 80.0, ... },
    "soft_skills": { "score": 76.0, ... }
  },
  "recommendations": [
    "Strong communication skills with clear articulation",
    "Demonstrates solid industry knowledge",
    "Could provide more specific examples"
  ]
}
```

---

## 🌍 多语言支持

### 当前支持

| 语言 | 代码 | 题库 | UI |
|------|------|------|----|
| English | en | ✅ | ✅ |
| 中文 | zh | ✅ | ✅ |
| Español | es | 🚧 | 🚧 |
| Français | fr | 🚧 | 🚧 |
| Deutsch | de | 🚧 | 🚧 |

> 🚧 = 开发中

### 题库文件命名规范

```
# 英文题库
english_proficiency.yaml

# 中文界面（候选人用英文回答）
english_proficiency_zh.yaml

# 完全本地化（待实现）
english_proficiency_es.yaml  # 西班牙语
```

---

## 🛠️ 开发指南

### 开发环境配置

#### 1. 克隆项目

```bash
git clone https://github.com/paulyupeng/intervieweragent.git
cd intervieweragent
```

#### 2. 配置环境

```bash
# 复制环境配置
cp .env.example .env

# 编辑 .env 填入 API 密钥
```

#### 3. 启动开发服务

```bash
# 方式 A: 使用 Docker Compose
docker-compose up -d

# 方式 B: 单独运行后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 单独运行前端
cd frontend
npm install
npm run dev
```

### 代码风格

#### Python
- 遵循 [PEP 8](https://pep8.org/)
- 使用类型注解
- 使用 `black` 格式化

```bash
pip install black
black backend/
```

#### TypeScript
- 使用 ESLint + Prettier
- 严格模式

```bash
cd frontend
npm run lint
npm run format
```

### 运行测试

```bash
# 后端测试（待添加）
cd backend
pytest

# 前端测试（待添加）
cd frontend
npm test
```

---

## 🚢 部署指南

### Docker 部署（推荐）

```bash
# 生产环境
docker-compose -f docker-compose.yml up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 环境变量配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `APP_ENV` | 运行环境 | `development` |
| `APP_SECRET_KEY` | JWT 密钥 | 必须修改 |
| `DATABASE_URL` | 数据库连接 | `postgresql://...` |
| `STORAGE_TYPE` | 存储类型 | `local` 或 `s3` |
| `MAX_INTERVIEW_DURATION_MINUTES` | 最大面试时长 | `60` |

### 生产部署检查清单

- [ ] 修改 `APP_SECRET_KEY`
- [ ] 配置 HTTPS
- [ ] 使用生产数据库
- [ ] 配置 S3 存储录音
- [ ] 设置日志收集
- [ ] 配置监控告警
- [ ] 定期备份数据库

---

## ❓ 常见问题

### Q: 面试录音保存在哪里？
**A:** 默认保存在 `backend/recordings/` 目录。可配置 `STORAGE_TYPE=s3` 使用 AWS S3 或兼容存储。

### Q: 如何自定义题库？
**A:** 编辑 `question_banks/` 目录下的 YAML 文件，或通过 Admin 界面管理。修改后重启后端服务生效。

### Q: 评分权重如何调整？
**A:** 访问 Admin → Scoring Configuration 页面调整，或修改数据库 `scoring_dimensions` 表。

### Q: 支持电话面试吗？
**A:** 当前版本仅支持 WebRTC 网页面试。电话集成（Twilio）在开发中。

### Q: 如何导出面试报告？
**A:** 在 Dashboard 点击 "Print Report" 可打印或保存为 PDF。导出 Excel/CSV 功能在开发中。

### Q: API 密钥获取？

**Deepgram:**
1. 访问 https://console.deepgram.com
2. 注册 → API Keys → Create Key

**ElevenLabs:**
1. 访问 https://elevenlabs.io
2. 注册 → Settings → Profile → API Key

**Anthropic:**
1. 访问 https://console.anthropic.com
2. 注册 → Get Keys

---

## 🗺️ 路线图

### v1.0 (当前版本) ✅
- [x] 语音面试核心功能
- [x] 多维度评分系统
- [x] JD-简历匹配
- [x] 基础管理后台

### v1.1 (Q2 2026) 🚧
- [ ] 电话面试集成 (Twilio)
- [ ] 视频分析（表情、肢体语言）
- [ ] 面试报告导出 (PDF/Excel)
- [ ] 批量面试（校园招聘）

### v1.2 (Q3 2026) 📋
- [ ] ATS 集成 (Greenhouse, Lever)
- [ ] 多人面试（面板面试）
- [ ] 自定义 AI 声音
- [ ] 面试模板库

### v2.0 (Q4 2026) 📋
- [ ] 人才库管理
- [ ] 协作评估（多面试官）
- [ ] 分析仪表板升级
- [ ] API 开放平台

---

## 🤝 贡献指南

欢迎贡献代码、文档或反馈问题！

### 贡献流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add your feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

### 开发设置

详见 [开发指南](#-开发指南)

### 代码规范

- Python: PEP 8 + 类型注解
- TypeScript: ESLint + Prettier
- 提交信息：[Conventional Commits](https://www.conventionalcommits.org/)

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)

---

## 📞 联系与支持

- **GitHub Issues**: [提交问题](https://github.com/paulyupeng/intervieweragent/issues)
- **讨论区**: [GitHub Discussions](https://github.com/paulyupeng/intervieweragent/discussions)
- **邮箱**: Paul.yupeng@gmail.com

---

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [Next.js](https://nextjs.org/) - React 全栈框架
- [LiveKit](https://livekit.io/) - 实时音视频 SDK
- [Deepgram](https://deepgram.com/) - 语音识别 API
- [ElevenLabs](https://elevenlabs.io/) - AI 语音合成
- [Anthropic](https://anthropic.com/) - Claude AI

---

<div align="center">

**Made with ❤️ by paulyupeng**

[⭐ Star this repo](https://github.com/paulyupeng/intervieweragent) | [Report Issue](https://github.com/paulyupeng/intervieweragent/issues)

</div>
