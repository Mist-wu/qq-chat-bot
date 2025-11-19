import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# 初始化 nonebot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 在这里加载插件
nonebot.load_from_toml("pyproject.toml") # 这会自动加载 src/plugins/ 下的插件

# 运行机器人
if __name__ == "__main__":
    nonebot.run()