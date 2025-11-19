from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.typing import T_State

# 导入您提供的AI逻辑模块
import chatAI
import database as db

# 创建一个事件处理器，响应所有消息
chat_handler = on_message(priority=10, block=False)

@chat_handler.handle()
async def handle_chat(bot: Bot, event: Event, state: T_State):
    # 从事件中获取用户ID和消息内容
    user_id = event.get_user_id()
    user_message = str(event.get_message()).strip()

    # 如果消息为空，则不处理
    if not user_message:
        return

    # 调用 get_response 函数获取AI回复
    # 注意：我们将 weather 相关的逻辑简化并移除了
    # 如果需要天气功能，建议使用Nonebot的天气插件或重写该部分
    try:
        ai_response = chatAI.get_response(user_id, user_message)
    except Exception as e:
        print(f"An error occurred while getting AI response: {e}")
        ai_response = "抱歉，AI出错了，请稍后再试。"

    # 将回复发送给用户
    if ai_response:
        await chat_handler.finish(Message(ai_response))