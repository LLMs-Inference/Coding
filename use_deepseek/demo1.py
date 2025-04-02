import os
import time

import openai
from openai import OpenAI


def get_completions(prompt):
    print("=" * 101)
    print(f"大语言模型提供商：DeepSeek!!   模型版本: DeepSeek-R1!!")

    # DeepSeek API 采用了与 OpenAI 兼容的 API 格式
    # 简单修改配置即可利用 OpenAI SDK 访问 DeepSeek API，或者使用其他与 OpenAI API 兼容的软件。
    client = OpenAI(
        api_key="sk-your_api_key******************************************",
        base_url="https://api.deepseek.com",
    )
    # deepseek-chat 和 deepseek-reasoner
    # print(client.models.list())

    messages_ = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="deepseek-reasoner",  # deepseek-chat 和 deepseek-reasoner
        messages=messages_,
        max_tokens=4096,
    )

    return response


print(f"OpenAI Python API 工具包的版本号：{openai.__version__}")

prompt_ = """
首先，您的任务是结合肿瘤系统生物学来深入解析芬顿反应（Fenton Reaction）的基本原理、重要作用以及在精准肿瘤学中的实际应用。
接着，在肿瘤系统生物学背景下深入分析代谢重编程（Metabolic Reprogramming）的基本原理、重要作用以及精准医疗意义。
最终，从因果关系的角度推断出芬顿反应与癌细胞代谢重编程之间是否存在合理的因果性调控关系（有方向）？
因果关系的定义：当且仅当在所有其他因素相同的情况下，t 的变化会导致 y 的相应变化时，变量 t 和 y 之间才存在因果关系。在分析和做出推断时，必须多思考并记住因果关系的本质。
""".strip()
print("=" * 101)
print(f"输入 Prompt：\n{prompt_}")

start_time = time.time()
result = get_completions(prompt_)
print(result)

print("=" * 101)
reasoning_content = result.choices[0].message.reasoning_content
print(f"生成的思维链内容：\n{reasoning_content}")

print("=" * 101)
content = result.choices[0].message.content
print(f"生成的答案：\n{content}")

end_time = time.time()
print(f"程序运行用时：{end_time - start_time}")
