# 这是一个简化的、基于内存的数据库，用于存储会话和用户设置。
# 注意：当程序关闭时，所有数据都会丢失。

_user_sessions = {}
_user_settings = {}

def get_user_session(user_id):
    """获取用户的会话历史"""
    return _user_sessions.get(user_id)

def update_user_session(user_id, session_data):
    """更新用户的会话历史"""
    _user_sessions[user_id] = session_data

def get_user_identity(user_id):
    """获取用户的身份ID"""
    return _user_settings.get(user_id, {}).get('identity_id', 0) # 默认为0

def get_user_setting(user_id, key):
    """获取用户设置"""
    return _user_settings.get(user_id, {}).get(key)

def update_user_setting(user_id, key, value):
    """更新用户设置"""
    if user_id not in _user_settings:
        _user_settings[user_id] = {}
    _user_settings[user_id][key] = value
