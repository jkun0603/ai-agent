# AI 大模型应用开发 —— 从零开始的学习路线

用 **Python + DeepSeek（云端 API）** 学习大模型应用开发的核心原理。
DeepSeek 是国内可直连、价格极低、且使用 **OpenAI 兼容接口**的模型服务 —— 现在学到的代码，
以后换任何一家（通义/智谱/Ollama/OpenAI/Claude）只需改 `config.py` 里 2 行，其余一行不用动。

> 可选路线：如果以后想**免费 + 本地跑**实验（不花一分钱），装个 [Ollama](https://ollama.com) 拉个本地模型，
> 同样只需改 `config.py` 的 `BASE_URL` 和 `MODEL`，本课程代码完全复用。

---

## 这套课程怎么用（学习方法）

1. **一课一脚本**：每课一个可运行的 `.py`，从上往下读注释 + 代码，然后自己运行。
2. **先观察，再理解**：每个脚本都故意把模型的"原始输出"打印出来，先看现象，再想原理。
3. **动手改参数**：每课末尾有「动手练习」，改一两个数字看效果变化 —— 这一步才是真正学会。
4. **带着问题学**：先看每课顶部「本课要回答的问题」，能回答出来 = 学会了。

> 学习顺序：`README` → `lessons/00_setup.md`（配置 DeepSeek）→ 从 `lesson_01` 往后一课一课跑。

---

## 阶段总览

| 阶段 | 课时 | 核心问题（学完能回答） | 学习内容 |
|------|------|------------------------|----------|
| **零、环境** | `00_setup.md` | 大模型服务到底怎么用？ | 注册 DeepSeek、拿 API key、配 `.env`、理解"调用大模型 = 发 HTTP 请求" |
| **一、第一次调用** | `lesson_01` | 一次对话请求长什么样？ | `client.chat.completions.create`、`system/user/assistant` 三种角色、返回的 JSON 结构 |
| **二、流式输出** | `lesson_02` | 为什么 ChatGPT 打字是一字一字蹦出来的？ | `stream=True`，token 逐个到达，像人打字一样 |
| **三、多轮对话** | `lesson_03` | 模型到底有没有"记忆"？ | 上下文 = 每次把全部历史 messages 再发给模型 |
| **四、生成参数** | `lesson_04` | 怎么让模型更"听话"或更有"创意"？ | `temperature` / `top_p` / `max_tokens` 的直观感受 |
| **五、提示词工程** | `lesson_05` | 不训练模型，怎么让它稳定输出我要的东西？ | 角色设定、few-shot、结构化 JSON、引导逐步思考 |
| **六、函数调用** | `lesson_06` | 模型怎么"调用代码"，而不是只会说话？ | Function Calling：模型输出调用意图 → 程序执行 → 回填结果 → 模型总结 |

> **进阶方向**（学完以上再进入，会单独开课）：
> RAG 知识库问答 → Agent 智能体（多步任务 + 工具循环）→ 用你会的 Vue / Spring Boot 做成网页产品。

---

## 核心心法（贯穿始终的 3 个概念）

1. **大模型是无状态的计算器**：它不记得任何历史。你发的每一条消息都是全新请求。
   所谓"记忆/多轮对话"，是你把历史聊天记录**自己攒起来、自己再发给它**。
   → 见 `lesson_03`

2. **模型只会"生成文字"，一切智能都靠 Prompt + 代码**：
   让它输出 JSON → 用提示词约束 + 代码解析。
   让它查天气 → 用 Function Calling 让模型调用你的 Python 函数。
   → 见 `lesson_05`、`lesson_06`

3. **现在调用的这套接口格式叫 OpenAI 兼容接口**，已经是行业事实标准。
   DeepSeek / 通义 / 智谱 / Ollama / OpenAI / Claude 几乎全用这一套代码，
   只改 `config.py` 的 `base_url`、`api_key`、`model`。
   → 见 `lessons/config.py`

---

## 快速开始

```bash
# 1) 拿 DeepSeek API key（一次性，约 2 分钟）
#    到 https://platform.deepseek.com 注册 → 左侧「API Keys」→ 创建
#    把 key 填进项目根目录的 .env 文件（已有模板，改一个值即可）

# 2) 激活本项目的虚拟环境
source .venv/Scripts/activate          # Windows Git Bash

# 3) 安装依赖（只需一次）
pip install -r requirements.txt

# 4) 跑第一课（每个脚本几十次调用总共几分钱）
python lessons/lesson_01_first_call.py
```

---

## 目录结构

```
ai 大模型应用/
├── README.md                    # 本文件：路线 + 方法
├── requirements.txt             # Python 依赖（目前只需 openai）
├── .env                         # 你的 DeepSeek API key（已被 .gitignore 保护）
├── .venv/                       # Python 虚拟环境（已建好）
└── lessons/
    ├── config.py                # 共用配置：连 DeepSeek、读 .env 里的 key（换厂商改这里）
    ├── 00_setup.md              # 环境准备：注册 DeepSeek、拿 key、验证
    ├── lesson_01_first_call.py  # 第一次调用（角色与请求结构）
    ├── lesson_02_streaming.py   # 流式输出（打字机效果）
    ├── lesson_03_multi_turn.py  # 多轮对话与上下文记忆
    ├── lesson_04_parameters.py  # temperature 等生成参数
    ├── lesson_05_prompt.py      # 提示词工程
    └── lesson_06_functions.py   # Function Calling（让模型调用你的代码）
```
