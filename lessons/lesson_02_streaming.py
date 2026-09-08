"""
Lesson 02 · 流式输出（Streaming）—— 打字机效果是怎么来的
========================================================

本课要回答的问题：
  1. 为什么 ChatGPT / 各种 AI 回答是"一个字一个字蹦出来"的？
  2. 一次性等全部结果 vs 边生成边显示，代码差在哪？

运行方式：
  python lessons/lesson_02_streaming.py

记住一句话：
  大模型本质是"一个字一个字地预测下一个字"。流式输出 = 它每算出一点，
  服务端就立刻发给你一点，而不是等你全部算完再一次性给你。
  用户体验会好非常多（首字快），也能实时展示进度。

技术细节（理解即可）：
  打开 stream=True 后，create() 不再返回一个完整 response，
  而是返回一个"生成器"，我们用 for 循环一次拿一个 chunk（一小段）。
  每个 chunk 里，新产生的文字放在 chunk.choices[0].delta.content，
  delta 是"增量"的意思 —— 只在这一次新增的内容。
"""

from config import MODEL, get_client

client = get_client()

messages = [
    {"role": "system", "content": "你是一个耐心的写作助手。"},
    {"role": "user", "content": "请给我讲一个关于程序员和咖啡的 3 句话小故事。"},
]

print("===== 流式输出（注意文字是一个字一个字出现的）=====\n")

# 关键就是这里：stream=True
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True,  # 👈 开启流式
)

# 流式模式下，response 是一个可迭代对象，逐个吐出小 chunk
full_text = ""
for chunk in response:
    # 每个 chunk 是一个片段，新增的文字在 delta.content 里
    piece = chunk.choices[0].delta.content
    if piece:  # 有时 chunk 里没有新文字（比如只是结束信号），要跳过
        full_text += piece
        print(piece, end="", flush=True)  # flush=True 保证立刻显示，不积攒在缓冲区

print("\n\n===== 拼接后的完整文本 =====")
print(full_text)
print(f"\n(共收到 {len(full_text)} 个字符)")

# ---------------------------------------------------------------
# 对照实验：如果不开 stream，会怎样？把下面取消注释对比体验：
#
#   response2 = client.chat.completions.create(
#       model=MODEL, messages=messages, stream=False,  # 默认就不开流式
#   )
#   print("\n非流式：一口气全出来 →", response2.choices[0].message.content)
#
# 结论：两个方式拿到的最终文字是一样的，区别只是"到达时间"。
# ---------------------------------------------------------------

# 动手练习：
#   1. 把故事要求改长一点（比如"写一篇 300 字的散文"），
#      感受流式让你不用干等几十秒。
#   2. 去掉 flush=True 运行一次，观察文字是不是"卡住后突然整段出现"，
#      这就是缓冲区在起作用 —— 也解释了为什么流式必须 flush。
# ---------------------------------------------------------------
