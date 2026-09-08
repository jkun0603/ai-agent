"""
Lesson 01 · 第一次调用大模型
==============================

本课要回答的问题：
  1. 一次对话请求，代码长什么样？
  2. 请求里的 messages 到底是什么？（三种角色：system / user / assistant）
  3. 模型返回的是什么？里面有哪些东西？

运行方式（先按 lessons/config.py 和 .env 配好 DeepSeek key）：
  python lessons/lesson_01_first_call.py

看完本课记住一句话：
  调用大模型 = 把我们和模型之间的一串对话(messages)发给一个 HTTP 服务，
  它返回"下一个回复"。什么缓存、记忆都没有 —— 一切都在 messages 里。
"""

# ---------------------------------------------------------------
# 第 1 步：创建一个"客户端"，让它知道去哪找模型服务
# ---------------------------------------------------------------
# 所有课程共用 lessons/config.py 里的配置（它已帮你连好 DeepSeek）。
# 想看看 config.py 做了什么？打开它读一遍 —— 你会明白"切换厂商只改一处"的妙处。
from config import MODEL, get_client

client = get_client()


# ---------------------------------------------------------------
# 第 2 步：组织消息 messages —— 这是理解大模型应用最关键的一步
# ---------------------------------------------------------------
# messages 是一份"聊天记录列表"，每条有 role 和 content 两个字段：
#
#   system（系统，可选）：
#       给模型设定身份和规则，模型会一直遵守。通常只放 1 条在最前面。
#       例：{"role": "system", "content": "你是一名经验丰富的 Python 老师"}
#
#   user（用户）：你说的每一句话。
#   assistant（助手）：模型之前回复过的内容。
#       注意：assistant 消息只有在"多轮对话"时才有用，见 lesson_03。
#       单轮请求里通常只有 system + user。
messages = [
    {"role": "system", "content": "你是一个说话简洁、略带幽默的 AI 助手。"},
    {"role": "user", "content": "请用一句话介绍你自己。"},
]


# ---------------------------------------------------------------
# 第 3 步：发送请求
# ---------------------------------------------------------------
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
)


# ---------------------------------------------------------------
# 第 4 步：看懂返回结果
# ---------------------------------------------------------------
# response 是一个结构体，模型真正的回答在：
#     response.choices[0].message.content
# 因为接口允许"一次返回多个候选回答"(choices)，我们通常取第 0 个。
reply = response.choices[0].message.content
print("===== 模型回复 =====")
print(reply)

# 为了帮你建立"这到底是个什么 JSON"的直觉，我们把它拆开看一看：
print("\n===== 返回结构解析（看懂这些 = 看懂所有大模型 API）=====")
print(f"回复的角色 role        : {response.choices[0].message.role}")
print(f"回复的内容 content     : {reply[:50]}...（这是最有用的字段）")
print(f"用到的模型 model       : {response.model}")
print(f"停止原因 finish_reason : {response.choices[0].finish_reason}   # stop=正常结束")
print(f"输入消耗 tokens        : {response.usage.prompt_tokens}")
print(f"输出消耗 tokens        : {response.usage.completion_tokens}")
print(f"总消耗 tokens          : {response.usage.total_tokens}")

# 💡 DeepSeek 每次调用都计费，想看用量/余额/账单去官网控制台：
print("\n👉 查看用量与余额：https://platform.deepseek.com  → 左侧『用量信息』")

# ---------------------------------------------------------------
# 动手练习：
#   1. 把 system 的内容改成"你是暴躁老哥，每句都用感叹号"，看看输出变化。
#   2. 删掉 system 那条消息，只留 user，看看有什么不同。
#   3. 把 user 问题换成"用 Python 写一个冒泡排序"，看它能不能给完整代码。
#   每次改完重跑这个文件即可（模型每次回答可能略有不同，正常）。
# ---------------------------------------------------------------
