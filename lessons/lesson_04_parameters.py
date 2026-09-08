"""
Lesson 04 · 生成参数 —— 怎么让模型更"听话"或更有"创意"
========================================================

本课要回答的问题：
  1. 模型每次回答为什么都不一样？怎么控制"稳定性 vs 发散"？
  2. temperature、top_p、max_tokens、seed 各管什么？

运行方式：
  python lessons/lesson_04_parameters.py

核心概念一句话：
  模型生成文字时，每一步其实是"在几百个候选词里按概率抽一个"。
  这些参数就是在调节【概率抽样的随机程度】：
    - temperature 高 → 更爱冒险、更有创意、但也更不可控
    - temperature 低 → 更保守、更稳定、接近"每次都选最可能那个词"
  实际项目里：写代码/取数(要正确)用低 temperature，写文案/脑洞(要发散)用高。
"""

from config import MODEL, get_client

client = get_client()

QUESTION = "用一句话形容：程序员周一早上打开电脑时的感受。"


def ask(extra: dict) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": QUESTION}],
        **extra,  # 把要测试的参数透传进去
    )
    return resp.choices[0].message.content


print("问：", QUESTION)
print("\n===== 实验 1：温度高 vs 温度低 =====")

print("\n--- temperature=0（几乎每次一样，求稳）---")
for _ in range(3):
    print("  ", ask({"temperature": 0.0}))

print("\n--- temperature=1.5（放飞自我，每次不同）---")
for _ in range(3):
    print("  ", ask({"temperature": 1.5}))


print("\n===== 实验 2：max_tokens —— 限制最多生成多少字 =====")
print("max_tokens 是输出长度上限（约等于 token 数，1 个中文字 ≈ 1~2 token）")
short = ask({"max_tokens": 15})
print("设 max_tokens=15，结果被截断：", short)


print("\n===== 实验 3：同样的题、同样的温度，模型每次答得一样吗？=====")
print("云端模型是分布式服务，同一句话常会算出不同结果 —— 这正是概率抽样的本质。\n"
      "（本地 Ollama 支持用 seed 固定随机种子实现'可复现'；DeepSeek 云端不开放 seed，\n"
      "  所以业务上要'稳定输出'靠的不是 seed，而是低 temperature + 写清楚的提示词。）")
for i in range(3):
    print(f"  第 {i+1} 次 (temperature=0.7)：{ask({'temperature': 0.7})}")


print("\n===== 小抄：参数速查 =====")
print("""
  temperature   0~2     越高越随机有创意，越低越稳定保守。DeepSeek 默认 1.0
  top_p         0~1     另一种随机控制：只从前 90% 概率的词里选。一般调一个即可
  max_tokens    整数    限制本次回复最大 token 数，防止废话 / 控制成本
  stop          字符串  遇到这个词就停止生成（比如让它输出到某个标记为止）
  seed          仅部分厂商支持（如本地 Ollama）；DeepSeek 云端不支持
""")

# ---------------------------------------------------------------
# 动手练习：
#   1. 把 QUESTION 换成一道数学题（如"13*17=? 只回答数字"），
#      分别用 temperature=0 和 1.5 各跑 5 次，看哪个正确率更高。
#   2. 这是理解"为什么代码任务要 temperature=0"的关键实验。
# ---------------------------------------------------------------
