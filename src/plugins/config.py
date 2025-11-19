# -- Cloudflare AI 配置 --
# 请替换为你的 Cloudflare Account ID 和 API Token
ACCOUNT_ID = "YOUR_CLOUDFLARE_ACCOUNT_ID"
AUTH_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"

# 使用的模型 (例如: llama-2-7b-chat-int8)
MODEL = "llama-2-7b-chat-int8"

# -- 聊天设置 --
# API 请求时附带的上下文消息长度
MAX_HISTORY_LEN = 6 

# -- 角色（Persona）配置 --
# 这里的配置与您原文件中的逻辑对应
# key 是 identity_id, file 是 prompt 目录下对应的文件名
PERSONAS = {
    "1": {"name": "猫娘", "file": "cat_girl.txt"},
    "2": {"name": "犬系男友", "file": "dog_boy.txt"},
    # 在这里可以添加更多角色
}