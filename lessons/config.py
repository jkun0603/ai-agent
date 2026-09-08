"""
config.py —— 所有课程共用的配置：连哪家大模型、API key 从哪来
================================================================

为什么要单独放一个 config.py？
  - API key 是秘密，不能写死在每个课程脚本里，否则很容易被误传到 GitHub。
  - 以后换厂商（Ollama/通义/智谱/OpenAI），只需要改这一个文件的 BASE_URL 和 MODEL，
    6 个课程脚本一行都不用动。

API key 读取顺序：
  1. 环境变量 DEEPSEEK_API_KEY
  2. 项目根目录的 .env 文件（推荐，见下面的使用说明）

使用说明（重要）：
  在【项目根目录】创建 .env 文件，内容一行：
      DEEPSEEK_API_KEY=你的key
  然后运行任意课程脚本即可。key 只在你自己电脑上使用。
"""

import os
import sys
from pathlib import Path

from openai import OpenAI

# Windows 中文控制台默认用 GBK 编码，无法打印表情等字符，会报 UnicodeEncodeError。
# 这里统一把标准输出切成 UTF-8，保证所有课程脚本在任何终端都能正常打印。
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ----------------------------------------------------------------------
# 厂商接入点。当前使用 DeepSeek（OpenAI 兼容接口）。
# 想切换厂商时改这里即可：
#   智谱 GLM  : BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
#   通义千问  : BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
#   本地 Ollama: BASE_URL = "http://localhost:11434/v1"  （MODEL 改成 ollama 里有的）
# ----------------------------------------------------------------------
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"   # DeepSeek 通用对话模型（另一个是 deepseek-reasoner，擅长深度推理）


def _load_dotenv_file():
    """手动解析项目根目录的 .env，把键值塞进环境变量（不引入额外第三方库）。"""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_api_key() -> str:
    _load_dotenv_file()
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "❌ 找不到 DeepSeek API key！\n\n"
            "   在项目根目录新建 .env 文件，写入：\n"
            "       DEEPSEEK_API_KEY=你的key\n\n"
            "   还没有 key？到 https://platform.deepseek.com 注册 → 左侧『API Keys』创建。\n"
            "   key 只保存在你本机，不会上传到任何地方。"
        )
    return key


def get_client() -> OpenAI:
    """返回一个已连好 DeepSeek 的客户端，供各课程脚本使用。"""
    return OpenAI(base_url=BASE_URL, api_key=get_api_key())


if __name__ == "__main__":
    # 自测：python lessons/config.py 应打印 key 的前 6 位
    k = get_api_key()
    print(f"config OK，检测到 key 以 {k[:6]}*** 开头，共 {len(k)} 位")
