"""
Lesson 06 · 函数调用（Function Calling）—— 让模型不只是"会说话"
================================================================

本课要回答的问题：
  1. 模型只会生成文字，怎么让它"动手做事"（查数据库 / 调接口 / 算结果）？
  2. Function Calling 的完整流程是什么？

运行方式：
  python lessons/lesson_06_functions.py

一个直击灵魂的类比：
  模型像一个【只会说不会做】的天才员工。你想让它订机票，
  它说"好的，我帮你订"。然后……就没下文了，因为它没法真的点按钮。

  Function Calling = 给这个员工配一个【工具箱】：
    1. 你告诉模型：箱子里有哪几个工具、每个工具是干嘛的、参数是什么；
    2. 模型分析用户需求后，**用文字返回**："我想用 订机票 这个工具，参数是北京→上海"；
    3. 【真正执行的是你的代码】——你去调航空公司接口，拿到结果；
    4. 你把结果放回对话里，再让模型基于真实结果总结给用户。

  一句话：模型只负责"决定调哪个工具、填什么参数"，真正的活是代码干的。

注意：
  我们用的 deepseek-chat 原生支持 function calling（工具调用）。
  若以后换了不支持的模型/厂商，现象会是"模型从不返回 tool_calls"，而不是报错。
"""

import json

from config import MODEL, get_client

client = get_client()


# =====================================================================
# 第 1 步：定义你真实存在的函数（工具背后的代码，真正干活的人）
# =====================================================================
# 这里我们用两个假函数模拟真实业务。真实场景里可能是查数据库/SQL、调天气 API 等。
def get_weather(city: str) -> str:
    """真实场景：调天气服务。这里返回模拟数据。"""
    fake = {"北京": "晴，26℃，适合出门", "上海": "小雨，23℃", "广州": "多云，30℃"}
    return fake.get(city, f"{city}：暂时没有该城市的数据，默认多云 25℃")


def get_stock_price(stock: str) -> str:
    """真实场景：查行情接口。这里返回模拟数据。"""
    fake = {"苹果": 191.5, "茅台": 1650, "腾讯": 380}
    return fake.get(stock, f"{stock}：暂无报价")


# =====================================================================
# 第 2 步：把工具"说明书"告诉模型（JSON Schema 格式，这是行业标准）
# =====================================================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的当天天气。当用户问天气时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如 北京"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "查询某支股票或公司的当前股价。当用户问股价/行情时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock": {"type": "string", "description": "股票或公司名，如 苹果"},
                },
                "required": ["stock"],
            },
        },
    },
]


# =====================================================================
# 第 3 步：写一个"模型要工具 → 我们执行 → 结果回填"的循环
# =====================================================================
def run_tool(name: str, args: dict) -> str:
    """根据模型要的工具名，调用真实的 Python 函数。"""
    if name == "get_weather":
        return get_weather(args["city"])
    if name == "get_stock_price":
        return get_stock_price(args["stock"])
    return "未知工具"


def chat_with_tools(user_input: str) -> str:
    """完整流程：模型决定调工具 -> 我们执行 -> 结果回填 -> 模型总结。"""

    # messages 里可以带 tools，模型就知道"我有工具可用"
    messages = [
        {"role": "system", "content": "你是生活助手。需要查天气/股价时就调用工具，"
                                      "拿到结果后用自然语言回复用户。"},
        {"role": "user", "content": user_input},
    ]

    # 第一轮：让模型自由发挥。它可能直接回答，也可能要求调用工具。
    resp = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto"
    )
    msg = resp.choices[0].message

    # 关键判断：模型是否想调用工具？（注意看 assistant 消息里有没有 tool_calls）
    if not msg.tool_calls:
        # 模型没想调用工具，直接回答了就完事
        return msg.content

    print(f"  🤖 模型决定调用工具：{msg.tool_calls[0].function.name} "
          f"参数={msg.tool_calls[0].function.arguments}")

    # 模型想调工具了：
    #  (a) 先把模型的这句话 append 进历史（带上 tool_calls），保持对话连贯
    messages.append(msg)
    #  (b) 逐个执行模型要的工具，把【执行结果】以 role="tool" 的消息回填
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        result = run_tool(tc.function.name, args)
        print(f"  ⚙️  代码执行 {tc.function.name}() → {result}")
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,          # 通过 id 把工具结果和那次调用对上
            "content": str(result),
        })

    #  (c) 带着"工具结果"再问一次模型，让它组织成人类语言回答
    second = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    return second.choices[0].message.content


# =====================================================================
# 第 4 步：试几个问题
# =====================================================================
print("问：北京今天天气怎么样，适合跑步吗？\n")
print("答：", chat_with_tools("北京今天天气怎么样，适合跑步吗？"), "\n")

print("-" * 60)
print("问：帮我查一下苹果和腾讯的股价。\n")
print("答：", chat_with_tools("帮我查一下苹果和腾讯的股价。"), "\n")

print("-" * 60)
print("问：随便讲个笑话吧。\n")
print("答：", chat_with_tools("随便讲个笑话吧。"), "\n")

# ---------------------------------------------------------------
# 动手练习：
#   1. 在 run_tool 里加一个你自己的函数（比如 get_phone_of_contact），
#      并在 TOOLS 里补上对应说明书，再让模型调用它。
#   2. 想想：为什么"工具参数从哪来、要几个"也是模型决定的？
#      这正是后面 Agent（自主完成多步骤任务）的核心 —— 模型+循环+工具。
# ---------------------------------------------------------------
