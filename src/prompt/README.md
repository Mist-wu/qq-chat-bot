## Prompt 文件说明

这个目录存放了不同AI角色的Prompt文本文件。

### 如何添加新角色？

1.  在此目录下创建一个新的 `.txt` 文件，例如 `my_persona.txt`。
2.  在文件中写入你想让AI扮演的角色的详细描述和要求。
3.  打开 `src/plugins/config.py` 文件。
4.  在 `PERSONAS` 字典中添加一个新的条目，例如：
    ```python
    PERSONAS = {
        "1": {"name": "猫娘", "file": "cat_girl.txt"},
        "2": {"name": "犬系男友", "file": "dog_boy.txt"},
        "3": {"name": "我的新角色", "file": "my_persona.txt"} # 添加这一行
    }
    ```
5.  之后，您可以通过命令或其他方式，将用户的 `identity_id` 设置为 `3`，机器人就会使用新的角色设定来回答问题。