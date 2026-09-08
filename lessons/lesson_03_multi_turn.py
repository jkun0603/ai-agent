"""
Lesson 03 · 多轮对话 —— 模型到底有没有"记忆"？
===============================================

本课要回答的问题：
  1. 和 AI 连续聊好几轮，它为什么"记得"我前面说了什么？
  2. 这个记忆是模型自带的，还是我们自己做的？

运行方式：
  python lessons/lesson_03_multi_turn.py

最重要的一个结论（务必记住）：
  大模型【没有任何记忆】。每一次调用都是"全新的一次请求"。
  所谓"多轮对话记忆"，是我们程序自己做的 ——
  把历史上【每一条 user 消息 + 每一条 assistant 回复】都存在一个列表里，
  每次提问时把【整份历史 + 新问题】一起发给模型。
  模型只是"看着这一整份文字"接着往下写而已。
"""

from config import MODEL, get_client

client = get_client()

# ------------------------------------------------------------------
# 我们用一个列表 messages 当"聊天记录本"，它就是模型的全部记忆来源
# ------------------------------------------------------------------
messages = [
    {"role": "system", "content": "你是一个帮用户记住偏好的贴心助手。"},
]


def ask(user_text: str) -> str:
    """模拟一次对话：把用户的话记进本子 -> 带着整本发给模型 -> 把回复也记进本子"""
    global messages

    # 1) 把用户新说的话追加到记录本
    messages.append({"role": "user", "content": user_text})

    # 2) 把【整本记录】发给模型（注意：发的永远是一整串历史）
    resp = client.chat.completions.create(model=MODEL, messages=messages)
    reply = resp.choices[0].message.content

    # 3) 把模型的回复也追加进记录本 —— 少了这步，下次模型就"看不见"自己说过的话
    messages.append({"role": "assistant", "content": reply})

    return reply


# ------------------------------------------------------------------
# 演示：连续三轮对话
# ------------------------------------------------------------------
print("===== 第 1 轮 =====")
print("我：我的名字叫小明，我最喜欢的编程语言是 Python。")
print("AI：" + ask("我叫小明，我最喜欢的编程语言是 Python。"))
print("\n此刻 messages 里有", len(messages), "条消息\n")

print("===== 第 2 轮 =====")
print("我：我刚才说我叫什么名字？")
print("AI：" + ask("我刚才说我叫什么名字？"))
print("\n此刻 messages 里有", len(messages), "条消息\n")

print("===== 第 3 轮 =====")
print("我：那顺便告诉我，Python 怎么打印 Hello World？")
print("AI：" + ask("顺便告诉我，Python 怎么打印 Hello World？"))

print("\n" + "=" * 50)
print("对照实验：如果不带历史记录，模型立刻'失忆' 👇")
fresh = client.chat.completions.create(
    model=MODEL,
    messages=[
        # 注意：这里只发了当前这一条，前面的 history 全部没带
        {"role": "user", "content": "我刚才说我叫什么名字？"},
    ],
)
print("AI（无历史）：", fresh.choices[0].message.content)
print("=" * 50)
print("看到区别了吧 —— 记忆 100% 来自 messages 历史列表，跟模型本身无关。")

# ---------------------------------------------------------------
# 动手练习：
#   1. 把上面"对照实验"的 messages 换成带历史的完整列表，看它是不是又记得了。
#   2. 想想：如果对话记录越来越长（超过模型上下文窗口），会发生什么？
#      这个问题就是后面学 RAG、上下文裁剪、摘要记忆的起点。
# ---------------------------------------------------------------
