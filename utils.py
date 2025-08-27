from langchain.prompts import ChatPromptTemplate
import os
from langchain_openai import ChatOpenAI
import requests

def get_baidu_summary(subject):
    """使用百度百科API获取摘要"""
    try:
        url = "https://baike.baidu.com/api/openapi/BaikeLemmaCardApi"

        params = {
            "scope": 103,
            "format": "json",
            "appid": 379020,
            "bk_key": subject
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("abstract"):
            return data["abstract"]  # 返回摘要内容
        else:
            return "百度百科未找到相关摘要"

    except Exception as e:
        return f"百度百科查询失败: {str(e)}"


def generate_script(subject, video_length, creativity, api_key, emotion, type, group):
    title_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'主题添加一个引人注目的主题")
        ]
    )
    script_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你现在是一名短视频博主，请你根据以下信息生成一个专业视频脚本框架，需包含以下结构化要素：
             目标观众：{group},
             视频类型:{type},
             时长范围：{duration}分钟，
             情感基调：{emotion}，
             生成的视频要遵循视频时长的要求，开头3s要快速抓住观众的眼球，内容要有干货，过程要有创意，结尾要有反转整体内容
             表达要符合当下人的生活习惯和精神需求，脚本格式要按照【开头、中间、结尾】分隔。
             脚本内容可以结合维基百科搜索的信息:'''{wikipedia_search}'''。但仅供参考，不相关的请忽略""")
        ]
    )

    model = ChatOpenAI(model = "deepseek-chat",
                       openai_api_key = api_key,
                       base_url = "https://api.deepseek.com/v1",
                       temperature = creativity)

    title_chain = title_prompt_template | model
    script_chain = script_prompt_template | model

    title = title_chain.invoke({"subject":subject}).content

    search_result = get_baidu_summary(subject)

    script = script_chain.invoke({"title":title, "group":group,"type":type, "duration":video_length,
                                  "emotion":emotion, "wikipedia_search":search_result} ).content

    return title, script, search_result

#generate = generate_script("电影", 1, 0.5, os.getenv("DEEPSEEK_API_KEY"),
#           "悲伤", "科普视频","文艺青年")
#print(generate)
