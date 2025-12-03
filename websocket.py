import asyncio
import websockets
import json

# --- 配置信息 ---
target_qq = "2550166270"
message_to_send = "你好，这是一条来自 Python 脚本的测试消息！"  
NAPCAT_HOST = "localhost"
NAPCAT_PORT = 3001
NAPCAT_TOKEN = "" # 您的访问令牌
# -----------------

async def send_private_message():
    """
    连接到需要身份验证的 NapCatQQ WebSocket 服务器并发送一条私聊消息。
    """
    uri = f"ws://{NAPCAT_HOST}:{NAPCAT_PORT}/ws"
    
    # 构建包含身份验证令牌的请求头
    headers = {
        "Authorization": f"Bearer {NAPCAT_TOKEN}"
    }
    
    print(f"正在连接到 NapCatQQ 服务器: {uri}")
    if NAPCAT_TOKEN:
        print("已配置访问令牌 (Token)。")

    try:
        # 【已修复】使用 extra_headers 关键字参数来传递请求头
        async with websockets.connect(uri, additional_headers=headers) as websocket:
            print("连接成功！身份验证通过。")

            # 构建 API 负载
            payload = {
                "action": "send_private_msg",
                "params": {
                    "user_id": int(target_qq), 
                    "message": message_to_send
                }
            }

            # 发送消息
            await websocket.send(json.dumps(payload))
            print(f"已发送消息到 QQ {target_qq}: '{message_to_send}'")

            # 等待并打印服务器响应
            response_str = await websocket.recv()
            response_json = json.loads(response_str)
            
            print("收到服务器响应:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 401:
            print(f"连接失败：身份验证错误 (Unauthorized)。请检查您的 Token (当前为: '{NAPCAT_TOKEN}') 是否正确。")
        else:
            print(f"连接失败，服务器返回 HTTP 状态码: {e.status_code}")
    except ConnectionRefusedError:
        print(f"连接被拒绝。请确保 NapCatQQ 正在 {NAPCAT_HOST}:{NAPCAT_PORT} 上运行。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    asyncio.run(send_private_message())