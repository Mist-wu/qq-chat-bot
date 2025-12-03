# ========= 导入必要模块 ==========
from ncatbot.core import BotClient, PrivateMessage, GroupMessage
from ncatbot.utils import config

config.set_bot_uin("2303188971")  # 设置 bot qq 号 (必填)
config.set_root("2550166270")  # 设置 bot 超级管理员账号 (建议填写)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_ws_token("")  # 设置 token (websocket 的 token)
config.set_webui_uri("http://localhost:6099")  # 设置 napcat webui 地址
config.set_webui_token("Yjcdi^}FO]5qsR)-")  # 设置 token (webui 的 token)

# ========== 创建 BotClient ==========
bot = BotClient()

# ========= 注册回调函数 ==========
@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    if msg.raw_message == "测试":
        await bot.api.post_private_msg(msg.user_id, text="Bot 测试成功")

@bot.group_event()
async def on_group_message(msg: GroupMessage):
    if msg.raw_message == "测试":
        await bot.api.post_group_msg(msg.group_id, text="Bot 测试成功")

# ========== 启动 BotClient==========
bot.run()