import config
import requests
import os
import database as db
# import weather  # 我们将在主插件中处理天气逻辑，所以这里暂时注释掉
import re # 导入正则表达式模块

    
def get_identity_prompt(identity_id):
    """根据身份ID获取对应的prompt内容。"""
    base_prompt = "你是一个名为'驱不散的雾'的AI助手。你的任务是友好、简洁地回答用户的问题。请始终使用简体中文回复。回复应像真人聊天，通常不超过100字。"

    if identity_id == 0:
        return base_prompt

    persona = config.PERSONAS.get(str(identity_id))
    if not persona: 
        return base_prompt

    filename = persona.get("file")
    if not filename:
        return base_prompt

    try:
        # 路径调整以适应插件结构
        filepath = os.path.join(os.path.dirname(__file__), '..', 'prompt', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            persona_prompt = f.read().strip()
            return persona_prompt
    except FileNotFoundError:
        return base_prompt

# 天气功能将由主插件处理，这里暂时移除 get_weather_report

def get_response(user_id, user_message):
    """获取AI回复，并管理会话历史。"""
    
    # 天气相关的逻辑已移至主插件，这里直接走标准聊天流程
    identity_id = db.get_user_identity(user_id)
    identity_prompt = get_identity_prompt(identity_id)
    
    history = db.get_user_session(user_id) or []
    messages_to_send = [{"role": "system", "content": identity_prompt}]
    
    history_for_api = history[-(config.MAX_HISTORY_LEN - 1):]
    messages_to_send.extend(history_for_api)
    
    messages_to_send.append({"role": "user", "content": user_message})

    ai_response = chat_with_cf(messages_to_send)

    if ai_response and not ai_response.startswith(("API返回错误:", "请求失败:", "网络请求异常:")):
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": ai_response})
        final_history_to_save = history[-config.MAX_HISTORY_LEN:]
        db.update_user_session(user_id, final_history_to_save)
    
    return ai_response

def chat_with_cf(messages):
    """调用Cloudflare AI API。"""
    if not all([config.ACCOUNT_ID, config.AUTH_TOKEN, config.MODEL]):
        return "网络请求异常: 服务器配置不完整，请联系管理员。"

    API_URL = f"https://api.cloudflare.com/client/v4/accounts/{config.ACCOUNT_ID}/ai/run/@cf/meta/{config.MODEL}"

    headers = {"Authorization": f"Bearer {config.AUTH_TOKEN}"}
    data = {"messages": messages}

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()

        result = response.json()
        if result.get('success') and result.get('result'):
            return result['result']['response'].strip()
        else:
            error_details = result.get('errors') or result.get('messages', '未知API错误')
            print(f"API Error: {error_details}")
            return f"API返回错误: {error_details}"
            
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}, {e.response.text}")
        return f"请求失败: 状态码 {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Network exception: {e}")
        return f"网络请求异常: {e}"