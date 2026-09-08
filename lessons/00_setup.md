# 第 0 课 · 环境准备：注册 DeepSeek + 配好 key

> 本课要解决的问题：
> 1. 我调用大模型，到底是在"调用什么"？
> 2. 为什么用 DeepSeek？怎么拿到 API key？怎么让课程代码用上它？

---

## 一、先搞懂：调用大模型 = 给一个远程服务发 HTTP 请求

任何大模型服务（DeepSeek / OpenAI / 通义 / 本地 Ollama）的本质都是：

> 有一台服务器运行着模型，对外开了一个 **HTTP 接口**。
> 你的 Python 程序通过网络发请求过去，把"文字输入"变成"文字输出"送回来。

DeepSeek 就是一家**云端**大模型服务商：
- 不用下载任何安装包，代码只通过 `openai` 这个库连它的服务器；
- 国内直连、速度快、价格极低（入门学习几十次调用总共几分钱，甚至远不到）；
- 接口用的是 **OpenAI 兼容格式** —— 行业事实标准，学会它等于学会了接所有主流厂商。

> 💡 对比理解：一开始我们本想用 Ollama（本机免费跑模型），但需要下载约 1.5GB 安装包 +
> 占本地内存。云端 API 免安装、免本地算力，只需要一个 key。两者代码 90% 相同，区别只在
> `config.py` 里 2 行配置。对新手入门，云端是更省事的路。

---

## 二、拿到 DeepSeek API key（约 2 分钟，只做一次）

1. 打开 https://platform.deepseek.com ，用手机号注册登录（新用户一般有免费赠送额度）。
2. 左侧菜单找到 **「API Keys」** → 点 **「创建 API Key」**。
3. 给它起个名（如 `study`），创建后会**显示一次**形如 `sk-xxxxxxxx` 的密钥 —— 立刻复制保存
   （关闭页面后不再显示，丢了只能重新创建）。
4. 顺手充一点点钱（¥10 就能学很久；新用户额度可能够你先免费跑完本课程）。

> ⚠️ key 就等于你的"账户密码"，**只放自己电脑的 `.env` 里**，别发群里/别提交到 GitHub。

---

## 三、把 key 填进本项目的 `.env`

项目根目录已有 `.env` 文件模板，用记事本/编辑器打开，把 `your_key_here` 换成你的真 key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

保存即可。课程代码（`lessons/config.py`）会自动读取它。

> `.env` 已被 `.gitignore` 忽略，不会被 `git add` 提交，放心填。

---

## 四、安装依赖并自测

在项目根目录执行：

```bash
source .venv/Scripts/activate        # 激活虚拟环境
pip install -r requirements.txt      # 只需 openai 一个库

# 自测：能读到 key 就成功
python lessons/config.py
# 期望输出：config OK，检测到 key 以 sk-*** 开头
```

---

## 五、写第一行代码前，最后确认一遍

在项目根目录执行一次真实调用，能收到回复就说明一切就绪：

```bash
python -c "from lessons.config import get_client; r=get_client().chat.completions.create(model='deepseek-chat', messages=[{'role':'user','content':'说“连接成功”四个字'}], max_tokens=10); print(r.choices[0].message.content)"
```

能打印出模型回复，就去 `lesson_01_first_call.py` 开始第一课吧！

---

## 常见问题排查

| 现象 | 原因 / 解法 |
|------|-------------|
| 报 `找不到 DeepSeek API key` | `.env` 没建，或 key 那行值还是 `your_key_here` |
| 报 `401 Authentication Fails` | key 填错了 / 多了空格。重开 `.env` 检查 |
| 报 `Insufficient Balance` | 账户余额不足，去官网充值（¥10 够学很久） |
| 报 `Connection timeout` | 网络连不上 api.deepseek.com。用国内网络一般没问题，别开全局代理试试 |
| 模型答得慢 | 正常。DeepSeek 在生成长文本时是流式的，体验见 lesson_02 |
